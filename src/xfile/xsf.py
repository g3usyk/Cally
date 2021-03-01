import bpy
from mathutils import Vector
from xml.etree import ElementTree as et


def generate_local(elem: et.Element, text) -> et.Element:
    tag = et.Element(f'local{elem.tag}')
    tag.text = text
    return tag


def generate_root(obj_count: int) -> et.Element:
    root = et.Element('bone')
    root.attrib['name'] = 'Root'
    root.attrib['numchilds'] = str(obj_count * 4)
    root.attrib['id'] = str(0)

    trans = et.Element('translation')
    trans.text = '0 0 0'
    rot = et.Element('rotation')
    rot.text = '0 0 0 1'
    loc_trans = generate_local(trans, trans.text)
    loc_rot = generate_local(rot, rot.text)

    p_id = et.Element('parentid')
    p_id.text = '-1'

    root.extend([trans, rot, loc_trans, loc_rot, p_id])
    for i in range(1, (obj_count * 4) + 1):
        c_id = et.Element('childid')
        c_id.text = str(i)
        root.append(c_id)
    return root


def generate_child(i: int, name: list, posn, rotation, scale: float):
    node = et.Element('bone')

    if len(name) == 1:
        node.attrib['name'] = f'{name[0]}{i}'
    else:
        node.attrib['name'] = f'{name[0]}{i}{name[1]}'

    node.attrib['numchilds'] = '3'
    node.attrib['id'] = f'{i + ((i - 1) * 4)}'

    trans = et.Element('trans')
    trans.text = f'{posn.x * scale} {posn.y * scale} {posn.z * scale}'
    rot = et.Element('rotation')
    rot.text = f'{rotation.x} {rotation.y} {rotation.z} {rotation.w}'
    loc_trans = generate_local(trans, '0 0 0')
    loc_rot = generate_local(rot, '0 0 0 1')

    p_id = et.Element('parentid')
    p_id.text = '0'

    node.extend([trans, rot, loc_trans, loc_rot, p_id])
    return node


def export_xsf(context, scale: float):
    objs = [obj for obj in context.selected_objects if obj.type == 'EMPTY']
    trans0 = Vector((0.0, 0.0, 0.0))

    root = et.Element('skeleton')
    root.attrib['numbones'] = str(len(objs) + 1)
    root.attrib['sceneambientcolor'] = '1 1 1'

    for i, obj in enumerate(objs, 1):
        posn = obj.location
        rotation = obj.rotation_quaternion
        handle = generate_child(i, ['handle'], posn, rotation, scale)
        seat = generate_child(i, ['seat', 'Sitting'], trans0, rotation, scale)
    pass
