from typing import Iterable, Sequence, Tuple
from xml.etree import ElementTree as et


class XFace:
    """Represents a face object as outlined in an xmf file.

    """

    def __init__(self, vertices: Iterable[Tuple[int, int]] = None):
        self.vertices = vertices
        if vertices is None:
            self.vertices = []

    def parse(self, vertex_ids: Sequence[Sequence[int]]) -> et.Element:
        """Concatenates a group of vertex index assignments into an xmf face tag.

        Args:
            vertex_ids (list): The assignments for each vertex to their corresponding vertex ids.

        Returns:
            An xml Element representing an xml <FACE> tag.

        """
        tag = et.Element('face')
        tag.attrib['vertexid'] = ' '.join([(str(vertex_ids[vertex[0]][vertex[1]])) for vertex in self.vertices])
        return tag
