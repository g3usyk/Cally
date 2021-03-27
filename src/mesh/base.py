import bpy
from mathutils import Vector
from ..maps.names import NameMap


class BaseMesh:
    """Prototypes behaviour for default mesh instantiation into Blender.

    """

    def __init__(self, name: str, vertices: list, faces: list,
                 uvs: list, norms: list, groups: list, morphs: dict = None):
        """

        Args:
            name (str): The name of the mesh.
            vertices (list): The position coordinates for each vertex.
            faces (list): The vertex indices for each face.
            uvs (list): The uv coordinates for each vertex.
            norms (list): The normal coordinates for each vertex.
            groups (list): The weights for each vertex.
            morphs (dict): The shape key morphs.
        """
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs
        self.norms = norms
        self.groups = groups
        self.morphs = morphs if morphs else {}

    def add_normals(self, obj: bpy.types.Object):
        if len(self.norms) > 0:
            obj.data.use_auto_smooth = True
            obj.data.normals_split_custom_set([(0, 0, 0) for _ in obj.data.loops])
            obj.data.normals_split_custom_set_from_vertices(self.norms)

    def add_uvs(self, obj: bpy.types.Object):
        """Generates uv coordinates for mesh object.

        Args:
            obj (bpy.types.Object): The blender object.
        """
        bpy.ops.mesh.uv_texture_add()
        if len(self.uvs) > 0:
            uvl = obj.data.uv_layers.active
            for face in obj.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[v_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y

    def add_groups(self, obj: bpy.types.Object):
        if len(self.groups) > 0:
            for vertex_id, group in enumerate(self.groups):
                for influence in group:
                    bone_id = influence[0]
                    if bone_id in NameMap.mapping:
                        bone_name = NameMap.lookup(bone_id)
                        if bone_name not in obj.vertex_groups:
                            obj.vertex_groups.new(name=bone_name)
                        obj.vertex_groups[bone_name].add([vertex_id], influence[1], 'ADD')

    def add_morphs(self, obj: bpy.types.Object):
        obj.shape_key_add(name='Basis')
        for morph, blend_vertices in self.morphs.items():
            shape_key = obj.shape_key_add(name=morph)
            for vertex_id, position in blend_vertices:
                new_position = Vector()
                new_position[:] = position
                shape_key.data[vertex_id].co = new_position

    def to_mesh(self, collection: bpy.types.Collection = None, smooth: bool = True, uvs: bool = True,
                norms: bool = False, groups: bool = False, morphs: bool = False):
        """Generates a mesh using raw geometric data.

        Args:
            collection (bpy.types.Collection): A collection to contain the mesh.
            smooth (bool): Whether or not to apply auto-smooth to the mesh.
            uvs (bool): Whether or not to include uv coordinates for the mesh.
            norms (bool): Whether or not to include custom vertex normals for the mesh.
            groups (bool): Whether or not to include vertex weights for the mesh.
            morphs (bool): Whether or not to include shape keys for the mesh.
        """
        if collection is None:
            collection = bpy.data.collections.get("Collection")

        mesh = bpy.data.meshes.new(self.name)
        obj = bpy.data.objects.new(mesh.name, mesh)

        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        mesh.from_pydata(self.vertices, [], self.faces)
        bpy.ops.object.select_all(action='DESELECT')

        if smooth:
            bpy.data.objects[mesh.name].select_set(True)
            bpy.ops.object.shade_smooth()
        if uvs:
            self.add_uvs(obj)
        if norms:
            self.add_normals(obj)
        if groups:
            self.add_groups(obj)
        if morphs:
            self.add_morphs(obj)
