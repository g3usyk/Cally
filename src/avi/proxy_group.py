import bpy
from .proxy import Proxy


class ProxyGroup:
    def __init__(self, *proxies):
        self.proxies = []
        for name, fpath in proxies:
            prox = Proxy(name, fpath)
            self.proxies.append(prox)

    def to_mesh(self, collection_name):
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
        for prox in self.proxies:
            prox.to_mesh(col)
        bpy.ops.object.select_all(action='DESELECT')
