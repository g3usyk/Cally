import bpy
from bpy.types import Collection, Object
from typing import Iterable, Mapping, Sequence, Tuple
from mathutils import Vector
from ..maps.names import NameMap


class BaseMesh:
    """Prototypes behaviour for default mesh instantiation into Blender.

    """

    def __init__(self, name: str, vertices: Sequence[Iterable[float]], faces: Iterable[Sequence[int]],
                 uvs: Sequence[Sequence[float]], norms: Sequence[Sequence[float]],
                 groups: Sequence[Iterable[Tuple[int, float]]],
                 morphs: Mapping[str, Iterable[Tuple[int, Iterable[float]]]] = None, material_id: int = None):
        """

        Args:
            name (str): The name of the mesh.
            vertices (list): The position coordinates for each vertex.
            faces (list): The vertex indices for each face.
            uvs (list): The uv coordinates for each vertex.
            norms (list): The normal coordinates for each vertex.
            groups (list): The weights for each vertex.
            morphs (dict): The shape key morphs.
            material_id (int): The material slot number for the mesh.
        """
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.uvs = uvs
        self.norms = norms
        self.groups = groups
        self.morphs = morphs if morphs else {}
        self.material_id = abs(material_id) if material_id is not None else -1

    def add_material(self, obj: Object) -> Object:
        mtl = bpy.data.materials.get(f'Material.{self.material_id}')
        if mtl is None:
            mtl = bpy.data.materials.new(name=f'Material.{self.material_id}')
            mtl.use_nodes = True
        if obj.data.materials:
            obj.data.materials[0] = mtl
        else:
            obj.data.materials.append(mtl)
        return obj

    def add_normals(self, obj: Object) -> Object:
        if len(self.norms) > 0:
            obj.data.use_auto_smooth = True
            obj.data.normals_split_custom_set([(0, 0, 0) for _ in obj.data.loops])
            obj.data.normals_split_custom_set_from_vertices(self.norms)
        return obj

    def add_uvs(self, obj: Object) -> Object:
        """Generates uv coordinates for mesh object.

        Args:
            obj (bpy.types.Object): The blender object.
        """
        obj.data.uv_layers.new()
        if len(self.uvs) > 0:
            uvl = obj.data.uv_layers.active
            for face in obj.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[v_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y
        return obj

    def add_groups(self, obj: Object) -> Object:
        if len(self.groups) > 0:
            for vertex_id, group in enumerate(self.groups):
                for influence in group:
                    bone_id = influence[0]
                    if bone_id in NameMap.mapping:
                        bone_name = NameMap.lookup(bone_id)
                        if bone_name not in obj.vertex_groups:
                            obj.vertex_groups.new(name=bone_name)
                        obj.vertex_groups[bone_name].add([vertex_id], influence[1], 'ADD')
        return obj

    def add_morphs(self, obj: Object) -> Object:
        basis = obj.shape_key_add(name='Basis')
        num_vertices = len(obj.data.vertices)
        
        for morph_name, blend_vertices in self.morphs.items():
            # CRITICAL: Reset ALL shape keys to 0 and ensure Basis is active
            # This prevents cascading deformations
            if obj.data.shape_keys:
                for kb in obj.data.shape_keys.key_blocks:
                    kb.value = 0.0
                obj.active_shape_key_index = 0
            
            shape_key = obj.shape_key_add(name=morph_name)
            for vertex_id, position in blend_vertices:
                if vertex_id < num_vertices:
                    new_position = Vector()
                    new_position[:] = position if position else [0, 0, 0]
                    shape_key.data[vertex_id].co = new_position
        
        # Activate Face.Average AFTER all shape keys are created
        if 'Face.Average' in self.morphs:
            face_avg_idx = obj.data.shape_keys.key_blocks.find('Face.Average')
            if face_avg_idx >= 0:
                obj.data.shape_keys.key_blocks[face_avg_idx].value = 1.0
                obj.active_shape_key_index = face_avg_idx
        return obj

    def add_mesh(self, collection: Collection) -> Object:
        bpy.ops.object.select_all(action='DESELECT')
        mesh = bpy.data.meshes.new(self.name)
        obj = bpy.data.objects.new(mesh.name, mesh)
        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        mesh.from_pydata(self.vertices, [], self.faces)
        bpy.context.view_layer.objects.active = None
        return obj

    def to_mesh(self, collection: Collection = None, smooth: bool = True, material: bool = False,
                uvs: bool = True, norms: bool = False, groups: bool = False,
                morphs: bool = False) -> Object:
        """Generates a mesh using raw geometric data.

        Args:
            collection (bpy.types.Collection): A collection to contain the mesh.
            smooth (bool): Whether or not to apply auto-smooth to the mesh.
            material (bool): Whether or not to include material id for the mesh.
            uvs (bool): Whether or not to include uv coordinates for the mesh.
            norms (bool): Whether or not to include custom vertex normals for the mesh.
            groups (bool): Whether or not to include vertex weights for the mesh.
            morphs (bool): Whether or not to include shape keys for the mesh.
        """
        if collection is None:
            collection = bpy.data.collections.get("Collection")
        obj = self.add_mesh(collection)
        if smooth:
            obj.select_set(True)
            bpy.ops.object.shade_smooth()
        if material:
            self.add_material(obj)
        if uvs:
            self.add_uvs(obj)
        if norms:
            self.add_normals(obj)
        if groups:
            self.add_groups(obj)
        if morphs:
            self.add_morphs(obj)
        return obj
