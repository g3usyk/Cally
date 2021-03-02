from mathutils import Vector
from xml.etree import ElementTree as et
from .prettify import pretty_print


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


def generate_child(ix: int, ix_offset: int, name: list, posn, rotation, scale: float):
    node = et.Element('bone')

    if len(name) == 1:
        node.attrib['name'] = f'{name[0]}{ix}'
    else:
        node.attrib['name'] = f'{name[0]}{ix}.{name[1]}'

    node.attrib['numchilds'] = '0'
    node.attrib['id'] = f'{ix + ix_offset + ((ix - 1) * 4)}'

    trans = et.Element('translation')
    trans.text = f'{posn.x * scale} {posn.y * scale} {posn.z * scale}'
    rot = et.Element('rotation')
    rot.text = f'{rotation.x} {rotation.y} {rotation.z} {rotation.w}'

    neg_posn = posn.copy()
    neg_posn.negate()
    loc_trans = generate_local(trans, f'{neg_posn.x * scale} {neg_posn.y * scale} {neg_posn.z * scale}')
    loc_rot = generate_local(rot, '0 0 0 1')

    p_id = et.Element('parentid')
    p_id.text = '0'

    node.extend([trans, rot, loc_trans, loc_rot, p_id])
    return node


def export_xsf(context, filepath: str, scale: float, pretty: bool):
    emptys = [obj for obj in context.selected_objects if obj.type == 'EMPTY']
    objs = [e for e in emptys if e.parent is None or len(e.children) > 0]

    root = et.Element('skeleton')
    root.attrib['numbones'] = str(len(objs) + 1)
    root.attrib['sceneambientcolor'] = '1 1 1'

    root.append(generate_root(len(objs)))

    for i, obj in enumerate(objs, 1):
        handle_posn = obj.matrix_world.to_translation()
        handle_rotation = obj.matrix_world.to_quaternion()
        seat_posn = handle_posn
        seat_rotation = handle_rotation

        pose_type = "Standing"
        if len(obj.children) > 0:
            spot = obj.children[0]
            if len(obj.children) > 1:
                for child in obj.children:
                    if len(child.children) == 0:
                        spot = child
                        break
            seat_posn = spot.matrix_world.to_translation()
            seat_rotation = spot.matrix_world.to_quaternion()

            spot_name = spot.name.split('.')
            if len(spot_name) > 1:
                pose_type = spot_name[1]

        handle = generate_child(i, 0, ['Handle'], handle_posn, handle_rotation, scale)
        seat = generate_child(i, 1, ['Seat', pose_type], seat_posn, seat_rotation, scale)
        catcher = generate_child(i, 2, ['Catcher'], handle_posn, handle_rotation, scale)
        pitcher = generate_child(i, 3, ['Pitcher'], handle_posn, handle_rotation, scale)
        root.extend([handle, seat, catcher, pitcher])

    xtext = et.tostring(root).decode('utf8')
    xtext = pretty_print(xtext) if pretty else xtext

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("<HEADER MAGIC=\"XSF\" VERSION=\"919\"/>")
        f.write("%s" % xtext)
