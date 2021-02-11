from xml.etree import cElementTree as et

class XVertex():
    def __init__(self, posn, norm, color, bone):
        self.posn = posn
        self.norm = norm
        self.uv = []
        self.color = color
        self.bone = bone

    def parse(self, idx, u_idx, scale):
        xvert = et.Element('vertex')
        xvert.attrib['numinfluences'] = '1'
        xvert.attrib['id'] = str(idx)

        xposn = et.Element('pos')
        xnorm = et.Element('norm')
        xcol = et.Element('color')
        xuv = et.Element('texcoord')
        xinf = et.Element('influence')

        xposn.text = ''.join([(str(p * scale) + ' ') for p in self.posn])[:-1]
        xnorm.text = ''.join([(str(n) + ' ') for n in self.norm])[:-1]
        xcol.text = ''.join([(str(c) + ' ') for c in self.color])[:-1]
        xuv.text = str(self.uv[u_idx][0]) + ' ' + str(abs(1 - self.uv[u_idx][1]))
        xinf.attrib['id'] = self.bone
        xinf.text = '1'

        xvert.append(xposn)
        xvert.append(xnorm)
        xvert.append(xcol)
        xvert.append(xuv)
        xvert.append(xinf)

        return xvert
