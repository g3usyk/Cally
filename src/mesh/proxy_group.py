from typing import Dict, Iterable, Tuple

import bpy
from bpy.types import Object

from .proxy import Proxy


class ProxyGroup:
    """Constructs multiple meshes under a single collection.

    """
    def __init__(self, proxies: Iterable[Tuple[str, Iterable[str]]]):
        self.proxies = []
        for name, fpath in proxies:
            prox = Proxy(name, fpath)
            self.proxies.append(prox)

    def to_mesh(self, collection_name: str, uvs: bool, weights: bool, morphs: bool) -> Dict[str, Object]:
        """Generates each mesh contained in the group.

        Args:
            collection_name (str): A string representing the containing collection.
            uvs (bool): Whether or not to include the mesh's uv coordinates.
            weights (bool): Whether or not to include the mesh's bone weights.
            morphs (bool): Whether ot not to include the mesh's morph shape keys.
        """
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
        objs = {}
        for prox in self.proxies:
            objs[prox.name] = prox.to_mesh(collection=col, uvs=uvs, groups=weights, morphs=morphs)
        bpy.ops.object.select_all(action='DESELECT')
        return objs
