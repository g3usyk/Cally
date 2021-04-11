from bpy.types import Context, Object
from mathutils import Quaternion, Vector
from typing import List, Sequence, Tuple
from xml.etree import ElementTree as et
from .utils import pretty_print
from ..maps.bones.heads import HeadMap
from ..maps.bones.rolls import RollMap
from ..xskel.xbone import XBone


def generate_offset(posn: Vector, rotation: Quaternion) -> Tuple[Vector, Quaternion]:
    offset = Quaternion((-0.5, 0.5, 0.5, 0.5))
    true_position = offset @ posn
    true_rotation = offset @ rotation
    true_rotation.invert()
    return true_position, true_rotation


def generate_attachment(obj: Object) -> et.Element:
    current_group = obj.vertex_groups.active
    bone_name = current_group.name if current_group and current_group.name in HeadMap.mapping else 'Female03MasterRoot'
    posn = HeadMap.lookup(bone_name)
    rot = Quaternion((0.5, 0.5, 0.5, 0.5)) @ Quaternion((0.0, 1.0, 0.0), RollMap.lookup(bone_name))
    attachment = XBone('AttachmentRoot', 0, posn[:], rot[:], -1)
    return attachment.write_bone()


def generate_root(name: str, count: int, category: str) -> et.Element:
    rotation = []
    children = [c for c in range(1, count + 1)]
    if category == 'FURNITURE':
        rotation = [0, 0, 0, 1]
    elif category == 'ROOM':
        rotation = [0.5, 0.5, 0.5, -0.5]
    root = XBone(name, 0, [0, 0, 0], rotation, -1, children)
    return root.write_bone()


def generate_child(bone_ix: int, name: Sequence[str], name_ix: int, posn: Vector,
                   rotation: Quaternion, scale: float) -> et.Element:
    posn = [(p * scale) for p in posn]
    rot = [rotation.x, rotation.y, rotation.z, rotation.w]
    if len(name) == 1:
        b_name = f'{name[0]}{name_ix:02d}'
    else:
        b_name = f'{name[0]}{name_ix:02d}.{name[1]}'
    child = XBone(b_name, bone_ix, posn, rot)
    return child.write_bone()


def generate_children(objs, id_offset: int, name_offset: int, scale: float, category: str) -> List[et.Element]:
    seats = []
    use_offset = False
    if category == 'ROOM':
        use_offset = True
    for i, spot in enumerate(objs, id_offset):
        posn = spot.matrix_world.to_translation()
        rot = spot.matrix_world.to_quaternion()
        if use_offset:
            posn, rot = generate_offset(posn, rot)
        spot_name = spot.name.split('.')
        spot_type = 'Standing'
        if 'sit' in spot_name[0].lower():
            spot_type = 'Sitting'
        seat = generate_child(i, ['Seat', spot_type], i - name_offset, posn, rot, scale)
        seats.append(seat)
    return seats


def generate_camera() -> List[et.Element]:
    camera_root = XBone('camera.01.01.root', 1,
                        [-2500, 750, 0], [0, 0.70707, 0, 0.70707])
    camera_target = XBone('camera.01.01.Target', 2,
                          [-500, 750, 0], [0.5, 0.5, 0.5, 0.5])
    return [camera_root.write_bone(), camera_target.write_bone()]


def generate_handle(handles: Sequence[Object], spots: Sequence[Object], ix: int, scale: float,
                    category: str) -> et.Element:
    if len(handles) > 0:
        node = handles[0]
    else:
        node = spots[0]
    posn = node.matrix_world.to_translation()
    rot = node.matrix_world.to_quaternion()
    name = 'Handle00'
    if category == 'ROOM':
        posn, rot = generate_offset(posn, rot)
        name = 'Seat01'
    handle = XBone(name, ix, [(p * scale) for p in posn], [rot.x, rot.y, rot.z, rot.w])
    return handle.write_bone()


def export_xsf(context: Context, filepath: str, category: str, scale: float):
    root = et.Element('skeleton')
    root.attrib['sceneambientcolor'] = '1 1 1'

    if category == 'ACCESSORY':
        obj = context.active_object
        root.extend(generate_attachment(obj))
    else:
        empty_objs = [obj for obj in context.selected_objects if obj.type == 'EMPTY']
        spots = [obj for obj in empty_objs if obj.empty_display_type != 'SPHERE']
        handles = [obj for obj in empty_objs if obj.empty_display_type == 'SPHERE']
        if category == 'FURNITURE':
            root.append(generate_root('Root', len(spots) + 1, category))
            root.append(generate_handle(handles, spots, 1, scale, category))
            root.extend(generate_children(spots, 2, 1, scale, category))
        elif category == 'ROOM':
            root.append(generate_root('Room', len(spots) + 3, category))
            root.extend(generate_camera())
            root.append(generate_handle(handles, spots, 3, scale, category))
            root.extend(generate_children(spots, 4, 2, scale, category))

    root.attrib['numbones'] = str(len(root))

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XSF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)
