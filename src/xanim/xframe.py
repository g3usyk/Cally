from typing import Sequence
from mathutils import Quaternion, Vector
from xml.etree import ElementTree as et
from ..maps.positions import PositionMap
from ..maps.rotations import RotationMap


class XFrame:
    def __init__(self, f_time: float, bone_name: str, rotation: Sequence[float],
                 translation: Sequence[float] = None):
        self.f_time = f_time
        self.bone_name = bone_name
        self.rotation = rotation
        self.translation = translation

    @staticmethod
    def compute_actual(default: Quaternion, difference: Quaternion) -> Quaternion:
        offset = Quaternion((difference.w, -difference.y, difference.z, -difference.x))
        actual = default @ offset
        return actual

    def compute_rotation(self) -> str:
        bone_quaternion = Quaternion((self.rotation[0], self.rotation[1],
                                      self.rotation[2], self.rotation[3]))
        if self.bone_name == 'PelvisNode':
            text = f'{-bone_quaternion.x} {-bone_quaternion.y} {-bone_quaternion.z} {bone_quaternion.w}'
        else:
            default_rotation = RotationMap.lookup(self.bone_name)
            default_quaternion = Quaternion((default_rotation[3], default_rotation[0],
                                             default_rotation[2], default_rotation[1]))
            true_rotation = self.compute_actual(default_quaternion, bone_quaternion)
            text = f'{true_rotation.x} {true_rotation.z} {true_rotation.y} {true_rotation.w}'
        return text

    def compute_translation(self, scale: float) -> str:
        bone_vector = Vector((self.translation[0], self.translation[1], self.translation[2]))
        default_translation = Vector(PositionMap.lookup(self.bone_name))
        true_translation = (default_translation + bone_vector) * scale
        return f'{true_translation.x} {true_translation.y} {true_translation.z}'

    def parse(self, scale: float) -> et.Element:
        tag = et.Element('keyframe')
        tag.attrib['time'] = str(self.f_time)
        if self.translation:
            trans_tag = et.Element('translation')
            trans_tag.text = self.compute_translation(scale)
            tag.append(trans_tag)
        rot_tag = et.Element('rotation')
        rot_tag.text = self.compute_rotation()
        tag.append(rot_tag)
        return tag
