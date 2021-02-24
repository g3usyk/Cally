import bpy
from .proxy import Proxy


class ProxyGroup:
    proxies = []

    def __init__(self, *proxies):
        for name, fpath in proxies:
            prox = Proxy(name, fpath)
            self.proxies.append(prox)

    def to_mesh(self, collection):
        coll = bpy.data.collections.new(collection)
        bpy.context.scene.collection.children.link(coll)
        for prox in self.proxies:
            prox.to_mesh(collection)
        bpy.ops.object.select_all(action='DESELECT')
