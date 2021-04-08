import bpy

from xml.etree import ElementTree as et
from .prettify import pretty_print
from ..xmesh.xmorph import XMorph


def generate_track(curve: bpy.types.FCurve, fps: int) -> et.Element:
    track = et.Element('track')
    name = curve.data_path.split('"')[1]
    track.attrib['morphname'] = XMorph.check_name(name)
    track.attrib['numkeyframes'] = str(len(curve.keyframe_points))
    for keyframe_point in curve.keyframe_points:
        frame, value = keyframe_point.co[:]
        keyframe = et.Element('keyframe')
        keyframe.attrib['time'] = str(frame / fps)
        weight = et.Element('weight')
        weight.text = str(value)
        keyframe.append(weight)
        track.append(keyframe)
    return track


def generate_tracks(obj: bpy.types.Object, fps: int):
    tracks = []
    for curve in obj.data.shape_keys.animation_data.action.fcurves:
        tracks.append(generate_track(curve, fps))
    return tracks


def export_xpf(context: bpy.types.Context, filepath: str, fps: int, frames: int):
    animated_objs = []
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj.data.shape_keys and obj.data.shape_keys.animation_data \
                and obj.data.shape_keys.animation_data.action:
            animated_objs.append(obj)

    root = et.Element('animation')
    for obj in animated_objs:
        root.extend(generate_tracks(obj, fps))

    root.attrib['numtracks'] = str(len(root))
    root.attrib['duration'] = str(frames / fps)

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XPF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)
