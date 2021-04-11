from typing import Iterable, List, Sequence
from xml.etree import ElementTree as et


class XBone:
    def __init__(self, name: str, bone_id: int, translation: Sequence[float], rotation: Sequence[float],
                 parent_id: int = 0, children: Iterable[int] = None):
        self.name = name
        self.b_id = bone_id
        self.translation = translation
        self.rotation = rotation
        self.parent_id = parent_id
        self.children = children if children is not None else []

    def apply_local_transform(self, values: Sequence[float], transform: str) -> List[float]:
        if transform == 'TRANSLATION':
            return [values[0], -values[2], -values[1]]
        else:
            return [values[0], values[1], values[2], -values[3]]

    def add_tag(self, root_tag: et.Element, tag_name: str, tag_text: str) -> et.Element:
        elem_tag = et.SubElement(root_tag, tag_name)
        elem_tag.text = tag_text
        return elem_tag

    def write_bone(self) -> et.Element:
        root = et.Element('bone')
        root.attrib['name'] = self.name
        root.attrib['numchilds'] = str(len(self.children))
        root.attrib['id'] = str(self.b_id)
        self.add_tag(root, 'translation', ' '.join([str(t) for t in self.translation]))
        self.add_tag(root, 'rotation', ' '.join([str(r) for r in self.rotation]))
        self.add_tag(root, 'localtranslation',
                     ' '.join([str(t) for t in self.apply_local_transform(self.translation, 'TRANSLATION')]))
        self.add_tag(root, 'localrotation',
                     ' '.join([str(r) for r in self.apply_local_transform(self.rotation, 'ROTATION')]))
        self.add_tag(root, 'parentid', str(self.parent_id))
        for child in self.children:
            self.add_tag(root, 'childid', str(child))
        return root
