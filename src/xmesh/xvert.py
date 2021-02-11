from xml.etree import cElementTree as et

class XVertex():
    def __init__(self):
        self.posn = []
        self.norm = []
        self.uv = []
        self.color = []
        self.bone = 0

    def parse(self, idx, u_idx, scale):
        xvert = et.Element('vertex')
        xvert.attrib['numinfluences'] = '1'
        xvert.attrib['id'] = str(idx)

        xposn = et.Element('pos')
        xposn.text = ''.join([(str(p * scale) + ' ') for p in self.posn])[:-1]
        xnorm = et.Element('norm')
        xnorm.text = ''.join([(str(n) + ' ') for n in self.norm])[:-1]
        xcol = et.Element('color')
        xcol.text = ''.join([(str(c) + ' ') for c in self.color])[:-1]
        xuv = et.Element('texcoord')
        xuv.text = str(self.uv[u_idx][0]) + ' ' + str(abs(1 - self.uv[u_idx][1]))
        xinf = et.Element('influence')
        xinf.attrib['id'] = self.bone
        xinf.text = '1'

        xvert.append(xposn)
        xvert.append(xnorm)
        xvert.append(xcol)
        xvert.append(xuv)
        xvert.append(xinf)

        return xvert
