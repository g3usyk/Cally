
from xml.etree import cElementTree as et

class XFace():
    def __init__(self):
        self.ix = []

    def parse(self, idxs):
        xfac = et.Element('face')
        xfac.attrib['vertexid'] = ''.join([(str(idxs[i[0]][i[1]]) + ' ') for i in self.ix])[:-1]
        return xfac
