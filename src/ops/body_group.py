from bpy.types import Object
from typing import Dict, Iterable, List, Tuple, Union
from itertools import repeat
from ..avi.proxy_group import ProxyGroup


class BodyGroup:
    """Abstracts creation of a group of body meshes.

    """

    def __init__(self, gender: str, parts: Iterable[Union[str, Iterable[str]]],
                 uvs: bool = True, weights: bool = True, morphs: bool = True):
        self.gender = gender.lower()
        self.parts = parts
        self.bl_idname = f'mesh.primitive_imvu_{self.gender}_body_add'
        self.bl_label = 'Body'
        self.bl_options = {'REGISTER', 'UNDO'}
        self.uvs = uvs
        self.weights = weights
        self.morphs = morphs

    def get_label(self, prefix: str, part: str) -> str:
        return f'{prefix}.{part.capitalize()}'

    def add_part(self, prefix: str, part: str) -> Tuple[str, List[str]]:
        label = self.get_label(prefix, part)
        file_path = ["assets", self.gender, f'{part}.pickle']
        return label, file_path

    def parent_parts(self, objs: dict, parent: str, parts: set):
        prefix = self.gender[0].upper()
        parent_obj = objs[self.get_label(prefix, parent)]
        body_parts = {self.get_label(prefix, p) for p in parts}
        for body_part in body_parts:
            obj = objs[body_part]
            obj.parent = parent_obj
            obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()

    @staticmethod
    def default_parts(gender: str) -> List[Object]:
        if gender == 'MALE':
            group = BodyGroup("male", [("head", "eyes", "brows", "lashes"),
                                       "torso", "hands", "legs", "calfs", "feet"])
        else:
            group = BodyGroup("female", [("head", "eyes", "brows", "lashes"),
                                         "torso", "hands", "thighs", "legs", "feet"])
        return list(group.execute(repeat(True)).values())

    def execute(self, selected_parts: Iterable[bool]) -> Dict[str, Object]:
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            selected_parts ():

        """
        proxies = []
        prefix = self.gender[0].upper()
        for selection, part in zip(selected_parts, self.parts):
            if selection:
                if isinstance(part, tuple):
                    for p in part:
                        proxies.append(self.add_part(prefix, p))
                else:
                    proxies.append(self.add_part(prefix, part))
        mesh_group = ProxyGroup(proxies)
        objs = mesh_group.to_mesh(f'{prefix}_Body', self.uvs, self.weights, self.morphs)
        return objs
