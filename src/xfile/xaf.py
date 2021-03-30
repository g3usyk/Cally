import bpy
from mathutils import Quaternion, Vector
from xml.etree import ElementTree as et
from .prettify import pretty_print
from ..maps.names import NameMap
from ..maps.positions import PositionMap
from ..maps.rotations import RotationMap
from ..xanim.xtrack import XTrack
from ..xanim.xframe import XFrame


def get_data_path(data_string: str):
    parts = data_string.split('.')
    bone_name = parts[1].split('"')[1]
    data_path = parts[-1]
    return bone_name, data_path


def get_keyframe_point(f_curve, data_path, keyframes):
    for key_points in f_curve.keyframe_points:
        frame, coord = key_points.co
        if frame not in keyframes[data_path]:
            keyframes[data_path][frame] = []
        keyframes[data_path][frame].append(coord)
    pass


def get_curves(obj):
    f_curves = {}
    for curve in obj.animation_data.action.fcurves:
        bone_name, data_path = get_data_path(curve.data_path)
        if bone_name not in f_curves:
            f_curves[bone_name] = {'location': {}, 'rotation_quaternion': {}}
        get_keyframe_point(curve, data_path, f_curves[bone_name])
    return f_curves


def process_animation(obj, fps: int):
    f_curves = get_curves(obj)
    tracks = []
    for bone_name, keyframes in f_curves.items():
        frames = []
        if bone_name != 'PelvisNode':
            for frame, coords in keyframes['rotation_quaternion'].items():
                keyframe = XFrame(frame / fps, bone_name, coords)
                frames.append(keyframe)
        else:
            for loc, rot in zip(keyframes['location'].items(), keyframes['rotation_quaternion'].items()):
                frame, loc_coords = loc
                _, rot_coords = rot
                keyframe = XFrame(frame / fps, bone_name, rot_coords, loc_coords)
                frames.append(keyframe)
        track = XTrack(bone_name, frames)
        tracks.append(track)
    return tracks


def process_pose(obj: bpy.types.Object) -> list:
    bones = [bone for bone in obj.pose.bones if bone.name in RotationMap.mapping]
    tracks = []
    for bone in bones:
        rotation = [coord for coord in bone.rotation_quaternion]
        translation = None
        if bone.name == 'PelvisNode':
            translation = [coord for coord in bone.location]
        keyframe = XFrame(0.0, bone.name, rotation, translation)
        track = XTrack(bone.name, [keyframe])
        tracks.append(track)
    return tracks


def export_xaf(context, filepath: str, scale: float, fps: int, debug: bool):
    obj = context.active_object
    root = et.Element('animation')

    tracks = []
    if obj.animation_data:
        tracks.extend(process_animation(obj, fps))
    else:
        tracks.extend(process_pose(obj))

    duration = context.scene.frame_end / fps
    root.attrib['numtracks'] = str(len(tracks))
    root.attrib['duration'] = str(duration)

    for track in tracks:
        root.append(track.parse(scale))

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext).upper() if debug else pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<HEADER MAGIC="XAF" VERSION="919" />')
        f.write("%s" % xtext)


def get_offset(original, default):
    difference = original @ default
    return Quaternion((difference.w, -difference.y,
                       -difference.x, difference.z))


def parse_rotation(keyframe: et.Element) -> Quaternion:
    rotation = keyframe.find('rotation').text
    rotation = [float(r) for r in rotation.split()]
    return Quaternion((rotation[3], rotation[0], rotation[1], rotation[2]))


def parse_translation(keyframe: et.Element) -> Vector:
    translation = keyframe.find('translation').text
    translation = [float(t) for t in translation.split()]
    return Vector((translation[0], translation[1], translation[2]))


def parse_track(obj: bpy.types.Object, track: et.Element, bone_id: int, scale: float, fps: int):
    bone_name = NameMap.lookup(bone_id)
    bone = obj.pose.bones[bone_name]
    default_rotation = RotationMap.lookup(bone_name)
    default = Quaternion((default_rotation[3], default_rotation[0],
                          default_rotation[1], default_rotation[2]))
    default.conjugate()
    is_animation = int(track.attrib['numkeyframes']) > 1
    for keyframe in track.iter('keyframe'):
        frame = float(keyframe.attrib['time']) * fps
        rotation = parse_rotation(keyframe)
        if bone_id == 1:
            bone.rotation_quaternion = Quaternion((rotation.w, -rotation.x, -rotation.y, -rotation.z))
            location = parse_translation(keyframe)
            default_location = Vector(PositionMap.lookup(bone_name)) * scale
            bone.location = (location - default_location) / scale
            if is_animation:
                bone.keyframe_insert(data_path="location", frame=frame)
        else:
            bone.rotation_quaternion = get_offset(rotation, default)
        if is_animation:
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)


def import_xaf(context, obj, filepath: str, scale: float, fps: int):
    data = ''
    with open(filepath, 'r') as f:
        data = f.read()
    data = data.lower()
    start = data.find('<animation')
    root = et.fromstring(data[start:])
    duration = float(root.attrib['duration'])
    for track in root.iter('track'):
        bone_id = int(track.attrib['boneid'])
        if bone_id in NameMap.mapping:
            parse_track(obj, track, bone_id, scale, fps)
    context.scene.frame_start = 0
    context.scene.frame_end = duration * fps
