import bmesh
import os
from xml.etree import ElementTree as et
from .prettify import pretty_print
from ..mesh.base import BaseMesh
from ..xmesh.xvert import XVertex
from ..xmesh.xface import XFace
from ..xmesh.xmap import WeightMap


def generate_vertices(obj, submap: dict, weight: str) -> list:
    """Constructs vertices with each representing an xmf vertex tag.

    Args:
        obj (): A bpy mesh object containing geometric data.
        submap (dict): A dictionary mapping each submesh to its corresponding bone and material ids.
        weight (str): A string determining bone weight assignment for all vertices.

    Returns:
        A list of vertex objects.

    """
    xverts = []

    groups = {g.index: WeightMap.get_bone_id(g.name) for g in obj.vertex_groups}

    xcol = ['1', '1', '1']
    bone_id = submap[obj.name][1]
    xinfls = {bone_id: 1}

    if weight == 'MANUAL':
        for v in obj.data.vertices:
            coords = obj.matrix_world @ v.co
            xcoords = [coords[0], coords[1], coords[2]]
            xnorms = [v.normal[0], v.normal[1], v.normal[2]]
            next_vert = XVertex(xcoords, xnorms, xcol, xinfls)
            xverts.append(next_vert)
    else:
        for v in obj.data.vertices:
            coords = obj.matrix_world @ v.co
            xcoords = [coords[0], coords[1], coords[2]]
            xnorms = [v.normal[0], v.normal[1], v.normal[2]]
            if len(v.groups) != 0:
                xinfls = {}
                for g in v.groups:
                    xinfls[str(groups[g.group])] = g.weight
            next_vert = XVertex(xcoords, xnorms, xcol, xinfls)
            xverts.append(next_vert)
    return xverts


def generate_faces(obj, verts: list) -> list:
    """Constructs faces with each representing an xmf face tag.

    Args:
        obj (): A bpy mesh object containing geometric data.
        verts (list): A list of vertex objects.

    Returns:
        A list of face objects.

    """
    xfaces = []

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    uv_layer = bm.loops.layers.uv.active

    for face in bm.faces:
        next_face = XFace()
        for v, l in zip(face.verts, face.loops):
            v_idx = v.index
            uv_coords = l[uv_layer].uv
            next_uv = [uv_coords[0], uv_coords[1]]
            if next_uv in verts[v_idx].uv:
                next_face.ix.append([v_idx, verts[v_idx].uv.index(next_uv)])
            else:
                next_face.ix.append([v_idx, len(verts[v_idx].uv)])
                verts[v_idx].uv.append(next_uv)
        xfaces.append(next_face)

    bm.free()
    return xfaces


def create_submesh(name: str, submap: dict, faces: list) -> et.Element:
    """Generates a submesh xmf tag.

    Args:
        name (str): A string referring to the name of the submesh.
        submap (dict): A dictionary mapping each submesh to its corresponding bone and material ids.
        faces (list): A list of face objects.

    Returns:
        An xml Element representing a single submesh.

    """
    sub = et.Element('submesh')
    sub.attrib['numfaces'] = str(len(faces))
    sub.attrib['numlodsteps'] = '0'
    sub.attrib['numsprings'] = '0'
    sub.attrib['nummorphs'] = '0'
    sub.attrib['numtexcoords'] = '1'
    sub.attrib['material'] = str(submap[name][2])
    return sub


def fill_submesh(sub: et.Element, verts: list, faces: list, scale: float):
    """Places xmf tags for vertices and faces into a submesh xmf tag.

    Args:
        sub (et.Element): An xml Element for a single submesh.
        verts (list): A list of vertex objects.
        faces (list): A list of face objects.
        scale (float): A float determining scaling factor for mesh on export.
    """
    v_id = 0
    v_ids = []
    for x in range(0, len(verts)):
        v_ids.append([])
        for y in range(0, len(verts[x].uv)):
            elem_vert = verts[x].parse(v_id, y, scale)
            sub.append(elem_vert)
            v_ids[x].append(v_id)
            v_id += 1
    sub.attrib['numvertices'] = str(v_id)
    for face in faces:
        elem_face = face.parse(v_ids)
        sub.append(elem_face)


def export_xmf(context, filepath: str, submap: dict,
               scale: float, weight: str, adv: bool):
    """Writes a new xmf file containing the selected meshes geometric data.

    Args:
        context (): A bpy context containing data in the current 3d view.
        filepath (str): A string pointing to the output location of the xmf file.
        submap (dict): A dictionary mapping each submesh to its corresponding bone and material ids.
        scale (float): A float determining scaling factor for mesh on export.
        weight (str): A string determining bone-weight assignment mode for all vertices.
        adv (bool): A boolean determining whether xmf file should be constructed using user input.
    """
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))

    mapping = submap
    if not adv:
        mapping = {}
        counts = []
        mtl = 0
        for obj in objs:
            posn = obj.matrix_world.translation
            assignments = ['', WeightMap.get_bone(posn)]
            count = len(obj.data.vertices)
            for c, material in counts:
                if count == c:
                    assignments.append(material)
                    break
            if len(assignments) == 2:
                assignments.append(mtl)
                counts.append((count, mtl))
                mtl += 1
            mapping[obj.name] = assignments
            if len(obj.vertex_groups) > 0:
                weight = 'AUTO'
        scale = 100.0

    for obj in objs:
        xverts = generate_vertices(obj, mapping, weight)
        xfaces = generate_faces(obj, xverts)

        sub = create_submesh(obj.name, mapping, xfaces)
        fill_submesh(sub, xverts, xfaces, scale)
        root.append(et.Comment(obj.name))
        root.append(sub)

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XMF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)


def extract(elem: et.Element, tag, conversion):
    child = elem.find(tag).text.split()
    values = [conversion(x) for x in child]
    return values


def extract_all(elem: et.Element, tag, conversion):
    children = elem.findall(tag)
    seen = set()
    values = []
    for child in children:
        k, v = int(child.attrib['id']), conversion(child.text)
        if (k, v) not in seen:
            values.append((k, v))
            seen.add((k, v))
    return values


def extract_submesh(sub: et.Element, name: str) -> BaseMesh:
    posns = []
    uvs = []
    norms = []
    infls = []
    for vert in sub.iter('vertex'):
        pos = extract(vert, 'pos', float)
        posns.append(tuple([p / 100 for p in pos]))
        norm = extract(vert, 'norm', float)
        norms.append(tuple(norm))
        # col = extract(vert, 'color', float)
        uv = extract(vert, 'texcoord', float)
        uvs.append((uv[0], abs(1 - uv[1])))
        infl = extract_all(vert, 'influence', float)
        infls.append(infl)
    loops = []
    for face in sub.iter('face'):
        vert_ids = [int(x) for x in face.attrib['vertexid'].split()]
        loops.append(vert_ids)
    return BaseMesh(name, posns, loops, uvs, norms, infls)


def import_xmf(filepath: str):
    """Parses submeshes from an xmf file.

    Args:
        context (): A bpy context containing data in the current 3d view.
        filepath (str): A string specifying the file path of the xml object.
    """
    data = ''
    with open(filepath, 'r') as f:
        data = f.read()
    data = data.lower()
    start = data.find('<mesh')
    root = et.fromstring(data[start:])
    objs = []
    obj_filepath = os.path.split(filepath)[1]
    obj_name = '.'.join(obj_filepath.split('.')[:-1])
    for sub in root.iter('submesh'):
        ob = extract_submesh(sub, obj_name)
        objs.append(ob)
    return objs
