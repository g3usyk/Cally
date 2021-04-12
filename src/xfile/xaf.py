from typing import AbstractSet, Dict, Iterable, List, Mapping, Tuple
from bpy.types import Context, FCurve, Object, PoseBone
from mathutils import Quaternion, Vector
from xml.etree import ElementTree as et
from .utils import pretty_print
from ..maps.groups import GroupMap
from ..maps.ids import IDMap
from ..maps.names import NameMap
from ..maps.positions import PositionMap
from ..maps.rotations import RotationMap
from ..xanim.xtrack import XTrack
from ..xanim.xframe import XFrame


def set_rotation_mode(obj: Object) -> Object:
    for bone in obj.pose.bones:
        bone.rotation_mode = 'QUATERNION'
    return obj


def get_data_path(data_string: str) -> Tuple[str, str]:
    data_elements = data_string.split('.')
    bone_name = data_elements[1].split('"')[1]
    data_path = data_elements[-1]
    return bone_name, data_path


def get_keyframe_point(f_curve: FCurve, data_path: str,
                       keyframes: Mapping[str, Dict[float, List[float]]]) -> Mapping[str, Dict[float, List[float]]]:
    for keyframe_points in f_curve.keyframe_points:
        frame, value = keyframe_points.co
        if frame not in keyframes[data_path]:
            keyframes[data_path][frame] = []
        keyframes[data_path][frame].append(value)
    return keyframes


def get_curves(obj: Object) -> Dict[str, Dict[str, Dict[float, List[float]]]]:
    f_curves = {}
    for curve in obj.animation_data.action.fcurves:
        bone_name, data_path = get_data_path(curve.data_path)
        if bone_name not in f_curves:
            f_curves[bone_name] = {'location': {}, 'rotation_quaternion': {}}
        get_keyframe_point(curve, data_path, f_curves[bone_name])
    return f_curves


def process_animation(obj: Object, bones: AbstractSet[str], fps: int) -> List[XTrack]:
    f_curves = get_curves(obj)
    tracks = []
    for bone_name, keyframes in f_curves.items():
        if bone_name in bones:
            frames = []
            if bone_name != 'PelvisNode':
                for frame, coords in keyframes['rotation_quaternion'].items():
                    keyframe = XFrame(frame / fps, bone_name, coords)
                    frames.append(keyframe)
            else:
                for location, rotation in zip(keyframes['location'].items(),
                                              keyframes['rotation_quaternion'].items()):
                    frame, location_coordinates = location
                    _, rotation_coordinates = rotation
                    keyframe = XFrame(frame / fps, bone_name, rotation_coordinates, location_coordinates)
                    frames.append(keyframe)
            track = XTrack(bone_name, frames)
            tracks.append(track)
    return tracks


def process_pose(obj: Object, bones: AbstractSet[str]) -> List[XTrack]:
    bones = [bone for bone in obj.pose.bones if bone.name in bones]
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


def export_xaf(context: Context, filepath: str, scale: float, selection: bool, fps: int, debug: bool):
    obj = context.active_object
    all_bones = set(RotationMap.mapping.keys())
    if selection:
        selected_bones = {bone.name for bone in context.selected_pose_bones}
        all_bones = all_bones.intersection(selected_bones)
    set_rotation_mode(obj)
    root = et.Element('animation')
    tracks = []
    if obj.animation_data:
        tracks.extend(process_animation(obj, all_bones, fps))
    else:
        tracks.extend(process_pose(obj, all_bones))
    duration = context.scene.frame_end / fps
    root.attrib['numtracks'] = str(len(tracks))
    root.attrib['duration'] = str(duration)
    for track in tracks:
        root.append(track.parse(scale))
    xml_text = et.tostring(root).decode('utf8')
    xml_text = pretty_print(xml_text).upper() if debug else pretty_print(xml_text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<HEADER MAGIC="XAF" VERSION="919" />')
        f.write("%s" % xml_text)


def set_timeline(context: Context, obj: Object, duration: float, fps: int, obj_animated: bool,
                 import_animated: bool) -> int:
    context.scene.frame_start = 0
    if obj_animated and import_animated:
        context.scene.frame_end = max(context.scene.frame_end, int(duration * fps))
    elif not obj_animated:
        context.scene.frame_end = int(duration * fps)
    return context.scene.frame_end


def get_selected_bones(selection: bool, selected_bone_groups: Iterable[str]):
    selected_bones = NameMap.mapping
    if selection:
        selected_bone_names = set()
        for bone_group in selected_bone_groups:
            selected_bone_names.update(GroupMap.lookup(bone_group))
        selected_bones = {IDMap.lookup(bone_name) for bone_name in selected_bone_names}
    return selected_bones


def reset_bone_keyframes(bone: PoseBone, rotation: Mapping[float, List[float]],
                         location: Mapping[float, List[float]]) -> PoseBone:
    for frame, _ in rotation.items():
        bone.keyframe_delete('rotation_quaternion', frame=frame)
    for frame, _ in location.items():
        bone.keyframe_delete('location', frame=frame)
    return bone


def reset_bone(bone: PoseBone, keyframes: Mapping[str, Mapping[float, List[float]]] = None) -> PoseBone:
    if keyframes is not None:
        reset_bone_keyframes(bone, keyframes['rotation_quaternion'], keyframes['location'])
    bone.lock_location[:] = False, False, False
    bone.location.zero()
    bone.rotation_mode = 'QUATERNION'
    bone.lock_rotation[:] = False, False, False
    bone.rotation_quaternion.identity()
    return bone


def get_rotation_offset(raw_rotation: Quaternion, default_rotation: Quaternion) -> Quaternion:
    rotation_difference = raw_rotation @ default_rotation
    return Quaternion((rotation_difference.w, -rotation_difference.y,
                       -rotation_difference.x, rotation_difference.z))


def parse_rotation(keyframe: et.Element) -> Quaternion:
    rotation = keyframe.find('rotation').text
    rotation = [float(r) for r in rotation.split()]
    return Quaternion((rotation[3], rotation[0], rotation[1], rotation[2]))


def parse_translation(keyframe: et.Element) -> Vector:
    translation = keyframe.find('translation').text
    translation = [float(t) for t in translation.split()]
    return Vector((translation[0], translation[1], translation[2]))


def parse_track(obj: Object, f_curves: Mapping[str, Mapping[str, Mapping[float, List[float]]]], track: et.Element,
                bone_id: int, scale: float, fps: int) -> Tuple[PoseBone, bool]:
    bone_name = NameMap.lookup(bone_id)
    bone = obj.pose.bones[bone_name]
    reset_bone(bone) if bone_name not in f_curves else reset_bone(bone, f_curves[bone_name])
    default_rotation = RotationMap.lookup(bone_name)
    default_quaternion = Quaternion((default_rotation[3], default_rotation[0],
                                     default_rotation[1], default_rotation[2]))
    default_quaternion.conjugate()
    is_animation = int(track.attrib['numkeyframes']) > 1
    for keyframe in track.iter('keyframe'):
        frame = int(float(keyframe.attrib['time']) * fps)
        raw_rotation = parse_rotation(keyframe)
        if bone_id == 1:
            bone.rotation_quaternion = Quaternion((raw_rotation.w, -raw_rotation.x,
                                                   -raw_rotation.y, -raw_rotation.z))
            raw_location = parse_translation(keyframe)
            default_location = Vector(PositionMap.lookup(bone_name)) * scale
            bone.location = (raw_location - default_location) / scale
            if is_animation:
                bone.keyframe_insert(data_path="location", frame=frame)
        else:
            bone.rotation_quaternion = get_rotation_offset(raw_rotation, default_quaternion)
        if is_animation:
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
    return bone, is_animation


def import_xaf(context: Context, obj: Object, filepath: str, scale: float, selection: bool,
               selected_bone_groups: Iterable[str], fps: int):
    selected_bones = get_selected_bones(selection, selected_bone_groups)
    with open(filepath, 'r') as f:
        data = f.read()
    data = data.lower()
    start = data.find('<animation')
    root = et.fromstring(data[start:])
    duration = float(root.attrib['duration'])
    f_curves = get_curves(obj) if obj.animation_data else {}
    obj_is_animated = True if obj.animation_data else False
    import_is_animated = False
    for track in root.iter('track'):
        bone_id = int(track.attrib['boneid'])
        if bone_id in selected_bones:
            bone, animated = parse_track(obj, f_curves, track, bone_id, scale, fps)
            import_is_animated = import_is_animated or animated
    set_timeline(context, obj, duration, fps, obj_is_animated, import_is_animated)
