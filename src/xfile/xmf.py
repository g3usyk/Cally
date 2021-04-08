import bpy
import bmesh
import os

from xml.etree import ElementTree as et

from .prettify import pretty_print
from ..maps.ids import IDMap
from ..maps.positions import PositionMap
from ..mesh.base import BaseMesh
from ..xmesh.xbvert import XBlendVertex
from ..xmesh.xface import XFace
from ..xmesh.xmorph import XMorph
from ..xmesh.xvert import XVertex


def generate_vertex(obj, vertex, colors: list, influences: dict) -> XVertex:
    location = obj.matrix_world @ vertex.co
    return XVertex(location[:], vertex.normal[:], colors, influences)


def generate_vertices(obj, bone_id: int, weight: str) -> list:
    """Construct xmf vertex objects from the given blender object.

    Args:
        obj (): A bpy mesh object containing geometric data.
        bone_id (int): A bone id to attach each vertex to.
        weight (str): The vertex bone-weight assignment method.

    Returns:
        list: The xmf vertex objects.

    """
    xverts = []
    color = ['1', '1', '1']
    influences = {str(bone_id): 1}

    if weight == 'OBJECT':
        for vertex in obj.data.vertices:
            next_vertex = generate_vertex(obj, vertex, color, influences)
            xverts.append(next_vertex)
    else:
        group_ids = {group.index: str(IDMap.lookup(group.name)) for group in obj.vertex_groups}
        for vertex in obj.data.vertices:
            if len(vertex.groups) != 0:
                influences = {}
                for g in vertex.groups:
                    influences[group_ids[g.group]] = g.weight
            next_vertex = generate_vertex(obj, vertex, color, influences)
            xverts.append(next_vertex)
    return xverts


def generate_blend_vertices(obj, vertices: list):
    if obj.data.shape_keys:
        key_blocks = obj.data.shape_keys.key_blocks
        for key_block in key_blocks[1:]:
            target_block_name = key_block.name
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()
            for i in range(len(key_blocks)):
                current_block_name = key_blocks[i].name
                current_block_idx = obj_copy.data.shape_keys.key_blocks.find(current_block_name)
                current_block = obj_copy.data.shape_keys.key_blocks[current_block_idx]
                if current_block_name != target_block_name:
                    obj_copy.shape_key_remove(current_block)
                else:
                    current_block.value = 1.0
            final_block = obj_copy.data.shape_keys.key_blocks[0]
            obj_copy.shape_key_remove(final_block)
            for i, vertex in enumerate(obj_copy.data.vertices):
                location = obj_copy.matrix_world @ vertex.co
                # normal = vertex.normal
                vertices[i].add_blend(target_block_name, location[:], vertex.normal[:])
            bpy.data.objects.remove(obj_copy)


def generate_triangulation(obj) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    return bm


def generate_faces(obj, vertices: list) -> list:
    """Constructs xmf format faces from the given object.

    Args:
        obj (): A bpy mesh object containing geometric data.
        vertices (list): The xmf vertex objects.

    Returns:
        list: A list of xmf face objects.

    """
    xfaces = []
    bm = generate_triangulation(obj)
    uv_layer = bm.loops.layers.uv.active
    for face in bm.faces:
        next_face = XFace()
        for vertex, loop in zip(face.verts, face.loops):
            vertex_id = vertex.index
            uv_coords = loop[uv_layer].uv
            next_uv = uv_coords[0], uv_coords[1]
            if next_uv in vertices[vertex_id].uv:
                next_face.vertices.append((vertex_id, vertices[vertex_id].uv.index(next_uv)))
            else:
                next_face.vertices.append((vertex_id, len(vertices[vertex_id].uv)))
                vertices[vertex_id].uv.append(next_uv)
        xfaces.append(next_face)
    bm.free()
    return xfaces


def generate_morphs(obj) -> dict:
    morphs = {}
    if obj.data.shape_keys:
        morphs = {key_block.name: XMorph(key_block.name) for key_block in obj.data.shape_keys.key_blocks[1:]}
    return morphs


def create_submesh(material: int, faces: int, morphs: int) -> et.Element:
    """Generates a submesh xmf tag.

    Args:
        material (int): A material index.
        faces (int): The number of xmf face objects.
        morphs (int): The number of xmf morph objects.

    Returns:
        et.Element: An xmf submesh tag.

    """
    sub = et.Element('submesh')
    sub.attrib['numfaces'] = str(faces)
    sub.attrib['numlodsteps'] = '0'
    sub.attrib['numsprings'] = '0'
    sub.attrib['nummorphs'] = str(morphs)
    sub.attrib['numtexcoords'] = '1'
    sub.attrib['material'] = str(material)
    return sub


def fill_submesh(submesh: et.Element, vertices: list, morphs: dict, faces: list, scale: float):
    """Places xmf tags for vertices and faces into a submesh xmf tag.

    Args:
        submesh (et.Element): An xmf tag for a single submesh.
        vertices (list): The xmf vertex objects.
        morphs (dict): The xmf morph objects.
        faces (list): The xmf face objects.
        scale (float): The scaling factor for the mesh on export.
    """
    current_vertex_id = 0
    vertex_ids = []
    for vertex_id in range(0, len(vertices)):
        vertex_ids.append([])
        for uv_id in range(0, len(vertices[vertex_id].uv)):
            vertex = vertices[vertex_id]
            vertex_tag = vertex.parse(current_vertex_id, uv_id, scale)
            submesh.append(vertex_tag)
            for morph_name, (position, normal) in vertex.blends.items():
                morphs[morph_name].vertices.append(XBlendVertex(current_vertex_id,
                                                                position, normal, vertex.uv[uv_id]))
            vertex_ids[vertex_id].append(current_vertex_id)
            current_vertex_id += 1
    submesh.attrib['numvertices'] = str(current_vertex_id)
    for morph in morphs.values():
        morph_tag = morph.parse(scale)
        submesh.append(morph_tag)
    for face in faces:
        face_tag = face.parse(vertex_ids)
        submesh.append(face_tag)


def skip_material(mtl: int) -> int:
    """Computes the next material index with respect to default avatar skin indices.

    Args:
        mtl (int): The current material index.

    Returns:
        int: The next material index to be used.
    """
    if mtl == 1 or mtl == 6:
        return mtl + 2
    return mtl + 1


def default_options(objs: list) -> tuple:
    body_part_ids = {'F.Feet': 7, 'F.Hands': 7, 'F.Head': 2, 'F.Legs': 7, 'F.Thighs': 7, 'F.Torso': 7,
                     'F.Eyes': 3, 'F.Lashes': 5, 'F.Brows': 8,
                     'M.Feet': 7, 'M.Hands': 7, 'M.Head': 2, 'M.Legs': 7, 'M.Calfs': 7, 'M.Torso': 7,
                     'M.Eyes': 3, 'M.Lashes': 5, 'M.Brows': 6}
    submap = {}
    material = 0
    scale = 100.0
    weight = 'OBJECT'
    for obj in objs:
        submap[obj.name] = {}
        if len(obj.vertex_groups) > 0:
            weight = 'VERTEX'
        location = obj.matrix_world.translation
        submap[obj.name]['bone'] = PositionMap.get_closest_bone(location)
        name = '.'.join(obj.name.split('.')[:2])
        if name in body_part_ids:
            submap[obj.name]['material'] = body_part_ids[name]
        else:
            submap[obj.name]['material'] = material
            material = skip_material(material)
    return submap, scale, weight


def write_xmf(filepath: str, objs: list, submap: dict, scale: float, weight: str):
    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))
    for obj in objs:
        vertices = generate_vertices(obj, submap[obj.name]['bone'], weight)
        generate_blend_vertices(obj, vertices)
        faces = generate_faces(obj, vertices)
        root.append(et.Comment(obj.name))
        morphs = generate_morphs(obj)
        sub = create_submesh(submap[obj.name]['material'], len(faces), len(morphs))
        fill_submesh(sub, vertices, morphs, faces, scale)
        root.append(sub)

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XMF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)


def export_xmf(context: bpy.types.Context, filepath: str, submap: dict,
               scale: float, weight: str, auto: bool):
    """Exports a new xmf file containing the selected submeshes' data.

    Args:
        context (bpy.types.Context): A bpy context containing data in the current 3d view.
        filepath (str): The filepath of the xmf file.
        submap (dict): A mapping where each submesh corresponds to a bone id and a material id.
        scale (float): The scaling factor for the mesh on export.
        weight (str): The vertex bone-weight assignment method.
        auto (bool): Whether or not to use automatically generated file output options.
    """
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
    if auto:
        submap, scale, weight = default_options(objs)
    write_xmf(filepath, objs, submap, scale, weight)


def apply_scale(value: str) -> float:
    return float(value) / 100


def extract(elem: et.Element, tag: str, conversion) -> list:
    child = elem.find(tag).text.split()
    values = [conversion(x) for x in child]
    return values


def extract_influences(elem: et.Element, tag: str, conversion) -> list:
    children = elem.findall(tag)
    seen = set()
    for influence in children:
        bone_id, weight = int(influence.attrib['id']), conversion(influence.text)
        seen.add((bone_id, weight))
    return list(seen)


def extract_morph_names(root: et.Element) -> dict:
    morphs = {}
    for morph in root.iter('morph'):
        morph_name = morph.attrib['name']
        morphs[morph_name.lower()] = morph_name
    for morph in root.iter('MORPH'):
        morph_name = morph.attrib['NAME']
        morphs[morph_name.lower()] = morph_name
    return morphs


def extract_morphs(sub: et.Element, morph_names: dict) -> dict:
    morphs = {}
    for morph in sub.iter('morph'):
        blend_vertices = []
        for blend_vertex in morph.iter('blendvertex'):
            vertex_id = int(blend_vertex.attrib['vertexid'])
            position = extract(blend_vertex, 'position', apply_scale)
            blend_vertices.append((vertex_id, position))
        alt_name = morph.attrib['name']
        morphs[morph_names[alt_name]] = blend_vertices
    return morphs


def extract_submesh(sub: et.Element, mesh_name: str, morph_names: dict) -> BaseMesh:
    positions = []
    uvs = []
    normals = []
    influences = []
    for vertex in sub.iter('vertex'):
        positions.append(extract(vertex, 'pos', apply_scale))
        normals.append(extract(vertex, 'norm', float))
        # col = extract(vert, 'color', float)
        uv = extract(vertex, 'texcoord', float)
        uvs.append((uv[0], abs(1 - uv[1])))
        influences.append(extract_influences(vertex, 'influence', float))
    morphs = extract_morphs(sub, morph_names)
    loops = []
    for face in sub.iter('face'):
        vertex_ids = [int(vertex_id) for vertex_id in face.attrib['vertexid'].split()]
        loops.append(vertex_ids)
    return BaseMesh(mesh_name, positions, loops, uvs, normals, influences, morphs)


def import_xmf(filepath: str):
    """Parses submeshes from an xmf file.

    Args:
        filepath (str): The filepath of the xml file.
    """
    data = ''
    with open(filepath, 'r') as f:
        data += f.read()
    data_copy = data.lower()
    start = data_copy.find('<mesh')
    morph_names = extract_morph_names(et.fromstring(data[start:]))
    root = et.fromstring(data_copy[start:])
    objs = []
    filename = os.path.split(filepath)[1]
    mesh_name = os.path.splitext(filename)[0]
    for submesh in root.iter('submesh'):
        obj = extract_submesh(submesh, mesh_name, morph_names)
        objs.append(obj)
    return objs
