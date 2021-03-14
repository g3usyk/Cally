from xml.etree import ElementTree as et


class XBone:
    def __init__(self, name, b_id, translation, rotation, parent_id=0, children=None):
        self.name = name
        self.b_id = b_id
        self.translation = translation
        self.rotation = rotation
        self.parent_id = parent_id
        self.children = children
        if self.children is None:
            self.children = []

    def local(self, values, transform):
        if transform == 'TRANSLATION':
            return [values[0], -values[2], -values[1]]
        else:
            return [values[0], values[1], values[2], -values[3]]

    def bone(self):
        bone_tag = et.Element('bone')
        bone_tag.attrib['name'] = self.name
        bone_tag.attrib['numchilds'] = str(len(self.children))
        bone_tag.attrib['id'] = str(self.b_id)
        return bone_tag

    def tag(self, tag_name, tag_text: str):
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
