from xml.etree import ElementTree as et


class XMorph:
    def __init__(self, name: str, morph_id: str = None):
        self.name = name
        self.morph_id = morph_id
        if not morph_id:
            self.morph_id = ''
        self.vertices = []

    @classmethod
    def check_name(cls, name: str) -> str:
        morph_name = name.replace(' ', '.').split('.')
        morph_type = morph_name[-1].upper()
        targets = {'ADDITIVE', 'AVERAGE', 'CLAMPED', 'EXCLUSIVE'}
        shorthand = {'ADD': 'Additive', 'AVG': 'Average', 'CL': 'Clamped', 'EX': 'Exclusive'}
        if morph_type in targets:
            morph_name[-1] = morph_type.title()
        elif morph_type in shorthand:
            morph_name[-1] = shorthand[morph_type]
        else:
            morph_name.append('Exclusive')
        return '.'.join(morph_name)

    def parse(self, scale: float) -> et.Element:
        tag = et.Element('morph')
        tag.attrib['name'] = XMorph.check_name(self.name)
        tag.attrib['morphid'] = str(self.morph_id)
        tag.attrib['numblendverts'] = str(len(self.vertices))
        for vertex in self.vertices:
            tag.append(vertex.parse(scale))
        return tag
