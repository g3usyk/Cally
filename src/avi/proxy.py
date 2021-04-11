import bpy
import inspect
import pickle
from bpy.types import Object
from typing import Iterable
from pathlib import Path
from ..mesh.base import BaseMesh


class Proxy(BaseMesh):
    """Constructs mesh by fetching binary pickle data.

    """
    relative_path = Path(inspect.getmodule(BaseMesh).__file__).parent

    def __init__(self, name: str, file_path: Iterable[str]):
        vertices = []
        faces = []
        uvs = []
        groups = []
        morphs = {}
        full_path = self.relative_path
        for fp in file_path:
            full_path = full_path / fp
        abs_path = full_path.absolute()
        with open(abs_path, "rb") as f:
            mapping = pickle.load(f)
            vertices = mapping['vertices']
            faces = mapping['faces']
            groups = mapping['groups']
            if 'uvs' in mapping:
                uvs = mapping['uvs']
            if 'morphs' in mapping:
                morphs = mapping['morphs']
        super().__init__(name=name, vertices=vertices, faces=faces, uvs=uvs, norms=[], groups=groups,
                         morphs=morphs)

    def add_uvs(self, obj: Object) -> Object:
        """Generates uv coordinates for mesh object.

        Args:
            obj (bpy.types.Object): The mesh object.
        """
        bpy.ops.mesh.uv_texture_add()
        if len(self.uvs) != 0:
            uvl = obj.data.uv_layers.active
            uv_idx = 0
            for face in obj.data.polygons:
                for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                    uv_x, uv_y = self.uvs[uv_idx]
                    uvl.data[l_idx].uv.x = uv_x
                    uvl.data[l_idx].uv.y = uv_y
                    uv_idx += 1
        return Object