import bmesh
from xml.etree import ElementTree as et
from src.xmesh.xvert import XVertex
from src.xmesh.xface import XFace
from src.xmesh.xmap import WeightMap
from src.xfile.prettify import pretty_print


def generate_vertices(obj, submap, weight):
    xverts = []
    verts = obj.data.vertices

    coords = [(obj.matrix_world @ v.co) for v in verts]
    norms = [v.normal for v in verts]

    xcol = ['1', '1', '1']
    bone_id = submap[obj.name][1]
    xinfls = {bone_id: 1}

    for x in range(0, len(verts)):
        xcoords = [coords[x][0], coords[x][1], coords[x][2]]
        xnorms = [norms[x][0], norms[x][1], norms[x][2]]
        if weight == 'AUTO':
            xinfls = {}
            infls = WeightMap.generate_influences(xcoords)
            for infl in infls:
                xinfls[infl[1]] = round(infl[0], 0)
        next_vert = XVertex(xcoords, xnorms, xcol, xinfls)
        xverts.append(next_vert)
    
    return xverts


def generate_faces(obj, verts):
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


def create_submesh(name, submap, faces):
    sub = et.Element('submesh')
    sub.attrib['numfaces'] = str(len(faces))
    sub.attrib['numlodsteps'] = '0'
    sub.attrib['numsprings'] = '0'
    sub.attrib['nummorphs'] = '0'
    sub.attrib['numtexcoords'] = '1'
    sub.attrib['material'] = str(submap[name][2])
    return sub


def fill_submesh(sub, verts, faces, scale):
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


def export_xmf(context, filepath, submap, scale, weight, pretty):
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))

    for obj in objs:
        xverts = generate_vertices(obj, submap, weight)
        xfaces = generate_faces(obj, xverts)

        sub = create_submesh(obj.name, submap, xfaces)
        fill_submesh(sub, xverts, xfaces, scale)
        root.append(et.Comment(obj.name))
        root.append(sub)

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext) if pretty else xtext

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XMF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)


def import_xmf(context, filepath):
    mesh = []
    with open(filepath, 'r') as f:
        pass
    pass
