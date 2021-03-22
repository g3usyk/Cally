import bpy
from mathutils import Quaternion, Vector
from xml.etree import ElementTree as et
from .prettify import pretty_print
from ..xanim.rmap import RotationMap
from ..xmesh.xmap import WeightMap


def compute_rotation(original, difference):
    offset = Quaternion((difference.w, -difference.y, difference.z, -difference.x))
    actual = original @ offset
    return actual


def generate_track(bone, scale):
    bone_id = WeightMap.get_bone_id(bone.name)

    track = et.Element('track')
    track.attrib['boneid'] = str(bone_id)
    track.attrib['numkeyframes'] = "1"

    keyframe = et.Element('keyframe')
    keyframe.attrib['time'] = "0"

    rotation = et.Element('rotation')
    default_rotation = RotationMap.lookup(bone.name)
    default_quaternion = Quaternion((default_rotation[3], default_rotation[0],
                                     default_rotation[2], default_rotation[1]))
    true_rotation = compute_rotation(default_quaternion, bone.rotation_quaternion)
    rotation.text = f'{true_rotation.x} {true_rotation.z} {true_rotation.y} {true_rotation.w}'

    if bone_id == 1:
        translation = et.Element('translation')
        original_translation = Vector(tuple(WeightMap.pmap['PelvisNode']))
        true_translation = original_translation + bone.location
        translation.text = ' '.join([str(t * scale) for t in true_translation])
        keyframe.append(translation)

    keyframe.append(rotation)
    track.append(keyframe)
    return track


def export_xaf(context, filepath: str, scale: float, debug: bool):
    obj = context.active_object
    bones = [b for b in obj.pose.bones if b.name in RotationMap.mapping]

    root = et.Element('animation')
    root.attrib['numtracks'] = str(len(bones))
    root.attrib['duration'] = "10"

    for bone in bones:
        track = generate_track(bone, scale)
        root.append(track)

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext).upper() if debug else pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<HEADER MAGIC="XAF" VERSION="919" />')
        f.write("%s" % xtext)


def parse_track(obj, track, mapping):
    bone_id = track.attrib['boneid']
    bone_name = mapping[bone_id]
    bone = obj.pose.bones[bone_name]
    default_rotation = RotationMap.lookup(bone_name)
    default_quaternion = Quaternion((default_rotation[3], default_rotation[0],
                                     default_rotation[1], default_rotation[2]))
    default_quaternion.conjugate()
    for keyframe in track.iter('keyframe'):
        original_rotation = keyframe.find('rotation').text
        original_rotation = [float(r) for r in original_rotation.split()]
        original_quaternion = Quaternion((original_rotation[3], original_rotation[0],
                                          original_rotation[1], original_rotation[2]))
        difference = original_quaternion @ default_quaternion
        bone.rotation_quaternion = Quaternion((difference.w, -difference.y,
                                               -difference.x, difference.z))


def import_xaf(obj, filepath: str):
    data = ''
    with open(filepath, 'r') as f:
        data = f.read()
    data = data.lower()
    start = data.find('<animation')
    root = et.fromstring(data[start:])
    mapping = {str(v): k for k, v in WeightMap.wmap.items()}
    for track in root.iter('track'):
        parse_track(obj, track, mapping)
