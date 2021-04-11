from typing import Collection
from xml.etree import ElementTree as et
from ..maps.ids import IDMap
from .xframe import XFrame


class XTrack:
    def __init__(self, bone_name: str, keyframes: Collection[XFrame] = None):
        self.bone_name = bone_name
        self.keyframes = keyframes if keyframes is not None else []

    def parse(self, scale: float):
        tag = et.Element('track')
        tag.attrib['boneid'] = str(IDMap.lookup(self.bone_name))
        tag.attrib['numkeyframes'] = str(len(self.keyframes))
        for keyframe in self.keyframes:
            tag.append(keyframe.parse(scale))
        return tag
