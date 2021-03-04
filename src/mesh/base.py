import bpy
from ..xmesh.xmap import WeightMap


class BaseMesh:
    """Prototypes behaviour for default mesh instantiation into Blender.

    """

    def __init__(self, name: str, vertices: list, faces: list,
                 uvs: list, norms: list, groups: list):
        """

        Args:
            name (str): A string representing the name of the mesh.
            vertices (list): A list containing x, y, and z position coordinates for each vertex.
            faces (list): A list containing vertex indices for each face.
            uvs (list): A list containing u, and v texture coordinates for each vertex.
            norms (list): A list containing s, and t normal coordinates for each vertex.
            groups (list): A list containing groups and weights for each vertex.
        """
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs
        self.norms = norms
        self.groups = groups

    def add_normals(self, ob):
        if len(self.norms) > 0:
            ob.data.use_auto_smooth = True
            ob.data.normals_split_custom_set([(0, 0, 0) for _ in ob.data.loops])
            ob.data.normals_split_custom_set_from_vertices(self.norms)

    def add_uvs(self, ob):
        """Generates uv coordinates for mesh object.

        Args:
            ob (): A bpy object without a uv map or uv coordinates.
        """
        bpy.ops.mesh.uv_texture_add()
        if len(self.uvs) > 0:
            uvl = ob.data.uv_layers.active
            for face in ob.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[v_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y

    def add_groups(self, ob):
        if len(self.groups) > 0:
            for bone_name, bone_id in WeightMap.wmap.items():
                ob.vertex_groups.new(name=bone_name)
            mapping = {v: k for k, v in WeightMap.wmap.items()}
            for i, group in enumerate(self.groups):
                for influence in group:
                    if influence[0] in mapping:
                        ob.vertex_groups[mapping[influence[0]]].add([i], influence[1], 'ADD')

    def to_mesh(self, collection=None, smooth=True, uvs=True, norms=False, groups=False):
        """Generates a mesh using raw geometric data.

        Args:
            collection (): A bpy collection in the scene to contain the mesh.
            smooth (bool): A boolean determining whether to apply auto-smooth to the mesh.
            uvs (bool): A boolean determining whether to include uv coordinates for the mesh.
            norms (bool): A boolean determining whether to include custom vertex normals for the mesh.
            groups (bool): A boolean determining whether to include vertex weights for the mesh.
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
        if norms:
            self.add_normals(ob)
        if groups:
            self.add_groups(ob)
