import inspect
import pickle
from pathlib import Path
from .base import BaseMesh


class Proxy(BaseMesh):
    """Constructs mesh by fetching binary pickle data.

    """
    relative_path = Path(inspect.getmodule(BaseMesh).__file__).parent

    def __init__(self, name: str, file_path):
        vertices = []
        faces = []
        uvs = []
        full_path = self.relative_path
        for fp in file_path:
            full_path = full_path / fp
        abs_path = full_path.absolute()
        with open(abs_path, "rb") as f:
            mapping = pickle.load(f)
            vertices = mapping['vertices']
            faces = mapping['faces']
            if 'uvs' in mapping:
                uvs = mapping['uvs']
        super().__init__(name, vertices, faces, uvs)

