import bmesh
from xml.etree import cElementTree as et
from src.xmesh.xvert import XVertex
from src.xmesh.xface import XFace

def export_xmf(context, filepath, submap, pretty, scale):
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))

    for obj in objs:
        coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
        norms = [v.normal for v in obj.data.vertices]
        xverts = []
        bone_id = submap[obj.name][1]
        if bone_id == "":
            bone_id = '0'
        for x in range(0, len(obj.data.vertices)):
            xcoords = [coords[x][0], coords[x][1], coords[x][2]]
            xnorms = [norms[x][0], norms[x][1], norms[x][2]]
            xcol = ['1', '1', '1']
            next_vert = XVertex(xcoords, xnorms, xcol, bone_id)
            xverts.append(next_vert)

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
                if next_uv in xverts[v_idx].uv:
                    next_face.ix.append([v_idx, xverts[v_idx].uv.index(next_uv)])
                else:
                    next_face.ix.append([v_idx, len(xverts[v_idx].uv)])
                    xverts[v_idx].uv.append(next_uv)
            xfaces.append(next_face)

        bm.free()

        sub = et.Element('submesh')
        sub.attrib['numfaces'] = str(len(xfaces))
        sub.attrib['numlodsteps'] = '0'
        sub.attrib['numsprings'] = '0'
        sub.attrib['nummorphs'] = '0'
        sub.attrib['numtexcoords'] = '1'
        sub.attrib['material'] = str(submap[obj.name][2])

        v_id = 0
        v_ids = []
        for y in range(0, len(xverts)):
            v_ids.append([])
            for z in range(0, len(xverts[y].uv)):
                elemvert = xverts[y].parse(v_id, z, scale)
                sub.append(elemvert)
                v_ids[y].append(v_id)
                v_id += 1

        sub.attrib['numvertices'] = str(v_id)

        for face in xfaces:
            elemface = face.parse(v_ids)
            sub.append(elemface)

        root.append(sub)

    xtext = et.tostring(root).decode('utf8')
    if pretty:
        xtext = xtext.upper()
        xtext = xtext.replace('<', '\n<')
        xtext = xtext.replace('\n</', '</')
    f = open(filepath, 'w', encoding='utf-8')
    f.write("<HEADER MAGIC=\"XMF\" VERSION=\"919\"/>")
    f.write("%s" % xtext)
    f.close()
