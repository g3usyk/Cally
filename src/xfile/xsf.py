from mathutils import Quaternion
from xml.etree import ElementTree as et
from .prettify import pretty_print
from ..xskel.xbone import XBone


def generate_root(name: str, count: int, category: str) -> et.Element:
    rot = []
    childs = [c for c in range(1, count + 1)]
    if category == 'FURNITURE':
        rot = [0, 0, 0, 1]
    elif category == 'ROOM':
        rot = [0.5, 0.5, 0.5, -0.5]
    root = XBone(name, 0, [0, 0, 0], rot, -1, childs)
    return root.write()


def generate_child(bone_ix: int, name: list, name_ix: int, posn, rotation, scale: float):
    posn = [(p * scale) for p in posn]
    rot = [rotation.x, rotation.y, rotation.z, rotation.w]
    if len(name) == 1:
        b_name = f'{name[0]}{name_ix:02d}'
    else:
        b_name = f'{name[0]}{name_ix:02d}.{name[1]}'
    child = XBone(b_name, bone_ix, posn, rot)
    return child.write()


def generate_children(objs, id_offset: int, name_offset: int, scale: float):
    seats = []
    for i, spot in enumerate(objs, id_offset):
        posn = spot.matrix_world.to_translation()
        rot = spot.matrix_world.to_quaternion()
        spot_name = spot.name.split('.')
        spot_type = 'Standing'
        if 'sit' in spot_name[0].lower():
            spot_type = 'Sitting'
        seat = generate_child(i, ['Seat', spot_type], i - name_offset, posn, rot, scale)
        seats.append(seat)
    return seats


def generate_camera():
    camera_root = XBone('camera.01.01.root', 1,
                        [-2500, 750, 0], [0, 0.70707, 0, 0.70707])
    camera_target = XBone('camera.01.01.Target', 2,
                          [-500, 750, 0], [0.5, 0.5, 0.5, 0.5])
    return [camera_root.write(), camera_target.write()]


def generate_origin():
    origin = XBone('Seat01.01.Standing', 3, [0, 0, 0], [0.5, 0.5, 0.5, 0.5])
    return origin.write()


def generate_handle(handles, spots, scale):
    if len(handles) > 0:
        node = handles[0]
    else:
        node = spots[0]
    posn = node.matrix_world.to_translation()
    rot = Quaternion((1.0, 0.0, 0.0, 0.0))
    handle = XBone('Handle01', 1, [(p * scale) for p in posn], [rot.x, rot.y, rot.z, rot.w])
    return handle.write()


def export_xsf(context, filepath: str, category: str, scale: float):
    objs = [obj for obj in context.selected_objects if obj.type == 'EMPTY']
    spots = [o for o in objs if o.empty_display_type != 'SPHERE']
    handles = [o for o in objs if o.empty_display_type == 'SPHERE']

    root = et.Element('skeleton')
    root.attrib['sceneambientcolor'] = '1 1 1'

    if category == 'FURNITURE':
        root.append(generate_root('Root', len(spots) + 1, category))
        root.append(generate_handle(handles, spots, scale))
        root.extend(generate_children(spots, 2, 1, scale))
    elif category == 'ROOM':
        root.append(generate_root('Room', len(spots) + 3, category))
        root.extend(generate_camera())
        root.append(generate_origin())
        # root.extend(generate_children(spots, 3, 0, scale))

    root.attrib['numbones'] = str(len(root))

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XSF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)
