import bpy


class BaseMesh:
    """Prototypes behaviour for default mesh instantiation into Blender.

    """
    def __init__(self, name: str, vertices: list, faces: list, uvs: list):
        """

        Args:
            name (str): A string representing the name of the mesh.
            vertices (list): A list of tuples containing x, y, and z position coordinates for each vertex.
            faces (list): A list of lists containing vertex indices for each face.
            uvs (list): A list of tuples containing u, and v texture coordinates for each vertex.
        """
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs

    def add_uvs(self, ob):
        """Generates uv coordinates to mesh object.

        Args:
            ob (): A bpy object without a uv map or uv coordinates.
        """
        if len(self.uvs) != 0:
            bpy.ops.mesh.uv_texture_add()
            uvl = ob.data.uv_layers.active
            uv_idx = 0
            for face in ob.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[uv_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y
                    uv_idx += 1

    def to_mesh(self, collection=None, smooth=True, uvs=True):
        """Generates a mesh using raw vertex, face, and uv data.

        Args:
            smooth (): A boolean determining whether to apply auto-smooth to the mesh.
            collection (): A bpy collection in the scene to contain the mesh.
        """
        if collection is None:
            collection = bpy.data.collections.get("Collection")

        mesh = bpy.data.meshes.new(self.name)
        ob = bpy.data.objects.new(mesh.name, mesh)

        collection.objects.link(ob)
        bpy.context.view_layer.objects.active = ob

        mesh.from_pydata(self.vertices, [], self.faces)
        bpy.ops.object.select_all(action='DESELECT')

        if smooth:
            bpy.data.objects[mesh.name].select_set(True)
            bpy.ops.object.shade_smooth()

        if uvs:
            self.add_uvs(ob)
