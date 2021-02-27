from xml.etree import ElementTree as et


class XFace:
    """Represents a face object as outlined in an xmf file.

    """

    def __init__(self):
        self.ix = []

    def parse(self, idxs):
        """Concatenates a group of vertex indices into an xmf face tag.

        Args:
            idxs (list): A list of lists of vertex indices.

        Returns:
            An xml Element representing an xml <FACE> tag.

        """
        xfac = et.Element('face')
        xfac.attrib['vertexid'] = ''.join([(str(idxs[i[0]][i[1]]) + ' ') for i in self.ix])[:-1]
        return xfac
