from xml.etree import ElementTree as et


class XBlendVertex:
    def __init__(self, vertex_id: int, position: list, normal: list, uv: list):
        self.vertex_id = vertex_id
        self.position = position
        self.normal = normal
        self.uv = uv

    def parse(self, scale: float) -> et.Element:
        tag = et.Element('blendvertex')
        tag.attrib['vertexid'] = str(self.vertex_id)
        tag.attrib['posdiff'] = ''

        xposn = et.Element('position')
        xposn.text = ' '.join([str(p * scale) for p in self.position])
        xnorm = et.Element('normal')
        xnorm.text = ' '.join([str(n) for n in self.normal])
        xuv = et.Element('texcoord')
        xuv.text = f'{self.uv[0]} {abs(1 - self.uv[1])}'

        tag.append(xposn)
        tag.append(xnorm)
        tag.append(xuv)

        return tag
