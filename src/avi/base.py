import bpy


class BaseMesh:
    def __init__(self, name, vertices, faces):
        self.name = name
        self.vertices = vertices
        self.faces = faces

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
