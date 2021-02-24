import inspect
import pickle
from pathlib import Path
from .base import BaseMesh


class Proxy(BaseMesh):
    relative_path = Path(inspect.getmodule(BaseMesh).__file__).parent

    def __init__(self, name, fpath):
        vertices = []
        faces = []
        uvs = []
        full_path = self.relative_path
        for fp in fpath:
            full_path = full_path / fp
        abs_path = full_path.absolute()
        with open(abs_path, "rb") as f:
            mapping = pickle.load(f)
            vertices = mapping['vertices']
            faces = mapping['faces']
            if 'uvs' in mapping:
                uvs = mapping['uvs']
        super().__init__(name, vertices, faces, uvs)

