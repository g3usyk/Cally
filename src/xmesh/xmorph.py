from xml.etree import ElementTree as et


class XMorph:
    def __init__(self, name: str, morph_id=None):
        self.name = name
        self.morph_id = morph_id
        if not morph_id:
            self.morph_id = ''
        self.vertices = []

    def parse(self, scale: float) -> et.Element:
        tag = et.Element('morph')
        tag.attrib['name'] = self.name
        tag.attrib['morphid'] = str(self.morph_id)
        tag.attrib['numblendverts'] = str(len(self.vertices))
        for vertex in self.vertices:
            tag.append(vertex.parse(scale))
        return tag
