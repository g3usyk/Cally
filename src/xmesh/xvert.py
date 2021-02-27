from xml.etree import ElementTree as et


class XVertex:
    """Represents a vertex object as outlined in a xmf file.

    """

    def __init__(self, posn, norm, color, infls):
        self.posn = posn
        self.norm = norm
        self.uv = []
        self.color = color
        self.infls = infls

    def parse(self, idx, u_idx, scale):
        """

        Args:
            idx ():
            u_idx ():
            scale ():

        Returns:
            An xml element representing an xmf <VERTEX> tag.

        """
        xvert = et.Element('vertex')
        xvert.attrib['numinfluences'] = str(len(self.infls))
        xvert.attrib['id'] = str(idx)

        xposn = et.Element('pos')
        xnorm = et.Element('norm')
        xcol = et.Element('color')
        xuv = et.Element('texcoord')

        xposn.text = ''.join([(str(p * scale) + ' ') for p in self.posn])[:-1]
        xnorm.text = ''.join([(str(n) + ' ') for n in self.norm])[:-1]
        xcol.text = ''.join([(str(c) + ' ') for c in self.color])[:-1]
        xuv.text = str(self.uv[u_idx][0]) + ' ' + str(abs(1 - self.uv[u_idx][1]))

        xvert.append(xposn)
        xvert.append(xnorm)
        xvert.append(xcol)
        xvert.append(xuv)

        for bone, infl in self.infls.items():
            xinf = et.Element('influence')
            xinf.attrib['id'] = bone
            xinf.text = str(infl)
            xvert.append(xinf)

        return xvert
