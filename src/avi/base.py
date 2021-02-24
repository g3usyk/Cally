import bpy


class BaseMesh:
    def __init__(self, name, vertices, faces, uvs):
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs

    def add_uvs(self, ob):
        bpy.ops.mesh.uv_texture_add()
        if len(self.uvs) != 0:
            uvl = ob.data.uv_layers.active
            uv_idx = 0
            for face in ob.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[uv_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y
                    uv_idx += 1

    def to_mesh(self, collection="Collection"):
        mesh = bpy.data.meshes.new(self.name)
        ob = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get(collection)
        col.objects.link(ob)
        bpy.context.view_layer.objects.active = ob
        mesh.from_pydata(self.vertices, [], self.faces)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[mesh.name].select_set(True)
        bpy.ops.object.shade_smooth()
        self.add_uvs(ob)
