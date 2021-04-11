from typing import Iterable, List, Sequence
from xml.etree import ElementTree as et


class XBone:
    def __init__(self, name: str, b_id: int, translation: Sequence[float], rotation: Sequence[float],
                 parent_id: int = 0, children: Iterable[int] = None):
        self.name = name
        self.b_id = b_id
        self.translation = translation
        self.rotation = rotation
        self.parent_id = parent_id
        self.children = children if children is not None else []

    def local(self, values: Sequence[float], transform: str) -> List[float]:
        if transform == 'TRANSLATION':
            return [values[0], -values[2], -values[1]]
        else:
            return [values[0], values[1], values[2], -values[3]]

    def bone(self) -> et.Element:
        bone_tag = et.Element('bone')
        bone_tag.attrib['name'] = self.name
        bone_tag.attrib['numchilds'] = str(len(self.children))
        bone_tag.attrib['id'] = str(self.b_id)
        return bone_tag

    def tag(self, tag_name: str, tag_text: str) -> et.Element:
        elem_tag = et.Element(tag_name)
        elem_tag.text = tag_text
        return elem_tag

    def write(self) -> et.Element:
        root = self.bone()
        trans = self.tag('translation', ' '.join([str(t) for t in self.translation]))
        rot = self.tag('rotation', ' '.join([str(r) for r in self.rotation]))
        loc_trans = self.tag('localtranslation',
                             ' '.join([str(t) for t in self.local(self.translation, 'TRANSLATION')]))
        loc_rot = self.tag('localrotation',
                           ' '.join([str(r) for r in self.local(self.rotation, 'ROTATION')]))
        p_id = self.tag('parentid', str(self.parent_id))
        root.extend([trans, rot, loc_trans, loc_rot, p_id])
        for child in self.children:
            root.append(self.tag('childid', str(child)))
        return root
