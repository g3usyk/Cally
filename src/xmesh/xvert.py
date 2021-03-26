from xml.etree import ElementTree as et


class XVertex:
    """Represents a vertex object following the xmf file format.

    """

    def __init__(self, position: list, normal: list, color: list, influences: dict):
        self.position = position
        self.normal = normal
        self.color = color
        self.influences = influences
        self.uv = []
        self.blends = {}

    def add_blend(self, name: str, position: list, normal: list):
        if position != self.position:
            self.blends[name] = position, normal

    def parse(self, vertex_id: int, uv_id: int, scale: float) -> et.Element:
        """

        Args:
            vertex_id ():
            uv_id ():
            scale ():

        Returns:
            An xml element representing an xmf <VERTEX> tag.

        """
        tag = et.Element('vertex')
        tag.attrib['numinfluences'] = str(len(self.influences))
        tag.attrib['id'] = str(vertex_id)

        xposn = et.Element('pos')
        xnorm = et.Element('norm')
        xcol = et.Element('color')
        xuv = et.Element('texcoord')

        xposn.text = ' '.join([(str(p * scale)) for p in self.position])
        xnorm.text = ' '.join([(str(n)) for n in self.normal])
        xcol.text = ' '.join([(str(c)) for c in self.color])
        xuv.text = f'{self.uv[uv_id][0]} {abs(1 - self.uv[uv_id][1])}'
        # xuv.text = str(self.uv[uv_id][0]) + ' ' + str(abs(1 - self.uv[uv_id][1]))

        tag.append(xposn)
        tag.append(xnorm)
        tag.append(xcol)
        tag.append(xuv)

        for bone, infl in self.influences.items():
            xinf = et.Element('influence')
            xinf.attrib['id'] = bone
            xinf.text = str(infl)
            tag.append(xinf)

        return tag
