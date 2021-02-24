import bpy


class BaseMesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

    def to_mesh(self, name):
        mesh = bpy.data.meshes.new(name)
        ob = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get("Collection")
        col.objects.link(ob)
        bpy.context.view_layer.objects.active = ob
        mesh.from_pydata(self.vertices, [], self.faces)
