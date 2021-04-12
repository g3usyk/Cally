import bpy
import random
from bpy.types import Object, PoseBone
from math import radians
from mathutils import Quaternion
from typing import Dict, Mapping, Set


def rand(num: float = 1) -> float:
    return random.uniform(radians(-num), radians(num))


def randq(coord: int, angle: float = 1, bound: float = None) -> Quaternion:
    axis = [0.0, 0.0, 0.0]
    axis[coord] = 1.0
    if bound is not None:
        return Quaternion(axis, random.uniform(radians(angle), radians(bound)))
    else:
        return Quaternion(axis, rand(angle))


def randomize_pelvis(bone: PoseBone, pose: str, gender: str) -> PoseBone:
    if pose == 'STAND':
        bone.location[:2] = random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)
        bone.rotation_quaternion = randq(2, 10)
        if gender == 'MALE':
            bone.rotation_quaternion @= randq(0, -20, -15) @ randq(1)
        else:
            bone.rotation_quaternion @= randq(0, -10, 0) @ random.choice([randq(1, 7.5, 12.5), randq(1, -12.5, -7.5)])
    else:
        bone.location[:] = rand(0.75), rand(0.1), random.uniform(-3.5, -2.5)
        if gender == 'MALE':
            bone.rotation_quaternion = randq(0, -100, -80) @ randq(1, 5) @ randq(2, 10)
        else:
            bone.rotation_quaternion = randq(0, -50, -15) @ randq(1, 5) @ randq(2, 20)
    return bone


def randomize_head(bones: Mapping[str, PoseBone], gender: str, spine: str) -> Mapping[str, PoseBone]:
    conjugate = random.choice([True, False])
    if conjugate:
        x_rotations = [randq(0, 0, 5).conjugated() for _ in range(4)]
    else:
        x_rotations = [randq(0, 0, 5) for _ in range(4)]
    bones['Neck01'].rotation_quaternion = x_rotations[0] @ randq(1) @ randq(2, 0, 5)
    bones['Neck02'].rotation_quaternion = x_rotations[1] @ randq(1) @ randq(2, -10, -5)
    bones['Neck03'].rotation_quaternion = x_rotations[2] @ randq(1) @ randq(2, 0, 2)
    bones['Neck04'].rotation_quaternion = x_rotations[3] @ randq(1) @ randq(2, 5, 10)
    bones['Head'].rotation_quaternion = randq(0, 10) @ randq(1, 45)
    if gender == 'MALE' or spine != 'SLOUCH':
        bones['Head'].rotation_quaternion @= randq(2, -10, 0)
    else:
        bones['Head'].rotation_quaternion @= randq(2, 20, 30)
    return bones


def randomize_male_spine(bones: Mapping[str, PoseBone], spine_type: str) -> Mapping[str, PoseBone]:
    if spine_type == 'STRAIGHT':
        bones['Spine01'].rotation_quaternion = randq(0, -11, -9) @ randq(1) @ randq(2, 5)
        bones['Spine02'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -1, -0.5)
        bones['Spine03'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -7.5, -5)
        bones['Spine04'].rotation_quaternion = randq(0, 5) @ randq(1) @ randq(2, -20, -15)
    elif spine_type == 'LEAN':
        bones['Spine01'].rotation_quaternion = randq(0, -24, -16) @ randq(1) @ randq(2, 5)
        bones['Spine02'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -20, -15)
        bones['Spine03'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -20, -15)
        bones['Spine04'].rotation_quaternion = randq(0, 5) @ randq(1) @ randq(2, -32, -27)
    elif spine_type == 'SLOUCH':
        bones['Spine01'].rotation_quaternion = randq(0, -60, -50) @ randq(1) @ randq(2, 5)
        bones['Spine02'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -10, -5)
        bones['Spine03'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -10, -5)
        bones['Spine04'].rotation_quaternion = randq(0, 5) @ randq(1) @ randq(2, -30, -25)
    else:
        pass
    return bones


def randomize_female_spine(bones: Mapping[str, PoseBone], spine_type: str, pelvis: float) -> Mapping[str, PoseBone]:
    if spine_type == 'STRAIGHT':
        if pelvis < 0:
            bones['Spine02'].rotation_quaternion = randq(0, -17, -12)
            bones['Spine03'].rotation_quaternion = randq(0, -7.5, -2.5)
        else:
            bones['Spine02'].rotation_quaternion = randq(0, 12, 17)
            bones['Spine03'].rotation_quaternion = randq(0, 2.5, 7.5)
        bones['Spine01'].rotation_quaternion = randq(0, 10, 15) @ randq(1) @ randq(2)
        bones['Spine02'].rotation_quaternion @= randq(1) @ randq(2)
        bones['Spine03'].rotation_quaternion @= randq(1) @ randq(2)
        bones['Spine04'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -20, -15)
    elif spine_type == 'LEAN':
        bones['Spine01'].rotation_quaternion = randq(0) @ randq(1) @ randq(2)
        bones['Spine02'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -27.5, -22.5)
        bones['Spine03'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -15, -10)
        bones['Spine04'].rotation_quaternion = randq(0, 7.5) @ randq(1, 15) @ randq(2, 10, 20)
    elif spine_type == 'SLOUCH':
        bones['Spine01'].rotation_quaternion = randq(0, -30, -25) @ randq(1) @ randq(2)
        bones['Spine02'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -15, -10)
        bones['Spine03'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -15, -10)
        bones['Spine04'].rotation_quaternion = randq(0) @ randq(1) @ randq(2, -30, -25)
    else:
        pass
    return bones


def randomize_spine(bones: Mapping[str, PoseBone], pose: str, gender: str, pelvis: Quaternion) -> str:
    if gender == 'MALE':
        if pose == 'STAND':
            spine_type = 'STRAIGHT'
        else:
            spine_type = random.choice(['LEAN', 'SLOUCH'])
        randomize_male_spine(bones, spine_type)
    else:
        if pose == 'STAND':
            spine_type = 'STRAIGHT'
        else:
            if pelvis.x > -0.3:
                spine_type = 'LEAN'
            else:
                spine_type = 'SLOUCH'
        randomize_female_spine(bones, spine_type, pelvis.y)
    return spine_type


def randomize_male_leg(bones: Mapping[str, PoseBone], side_name: str) -> Mapping[str, PoseBone]:
    bones['Calf'].rotation_quaternion @= randq(0, 4, 8)
    bones['Thigh'].rotation_quaternion = randq(0, 5, 25)
    if side_name == 'rt':
        bones['Thigh'].rotation_quaternion @= randq(1, 10, 30) @ randq(2, -5, 20)
    else:
        bones['Thigh'].rotation_quaternion @= randq(1, -30, -10) @ randq(2, -20, 5)
    return bones


def randomize_female_leg(bones: Mapping[str, PoseBone], side_name: str, pelvis: float,
                         leg_order: str) -> Mapping[str, PoseBone]:
    bones['Calf'].rotation_quaternion @= randq(0, 20, 24) if leg_order == 'FORWARD' else randq(0, 4, 8)
    if pelvis < 0:
        bones['Thigh'].rotation_quaternion = randq(2, -5, 0) if side_name == 'rt' else randq(2, 5, 15)
    else:
        bones['Thigh'].rotation_quaternion = randq(2, -20, -15) if side_name == 'rt' else randq(2, -5, 0)
    bones['Thigh'].rotation_quaternion @= randq(1, -10, 0)
    bones['Thigh'].rotation_quaternion @= randq(0, -15, -5) if leg_order == 'FORWARD' else randq(0, 5, 15)
    return bones


def randomize_leg(bones: Mapping[str, PoseBone], side_name: str, pose: str, gender: str, pelvis: float,
                  leg_order: str = None) -> Mapping[str, PoseBone]:
    bones['Foot'].rotation_quaternion = randq(0, 0, 4) @ randq(1, 8) @ randq(2, 8)
    if pose == 'STAND':
        bones['Calf'].rotation_quaternion = randq(1) @ randq(2)
        if gender == 'MALE':
            randomize_male_leg(bones, side_name)
        else:
            randomize_female_leg(bones, side_name, pelvis, leg_order)
    elif pose == 'SIT':
        bones['Calf'].rotation_quaternion = randq(0, 30, 120) @ randq(1) @ randq(2)
        if gender == 'MALE':
            bones['Thigh'].rotation_quaternion = randq(0, 25)
            if side_name == 'rt':
                bones['Thigh'].rotation_quaternion @= randq(1, 0, 60) @ randq(2, 20, 50)
            else:
                bones['Thigh'].rotation_quaternion @= randq(1, -60, 0) @ randq(2, -30, 0)
        else:
            bones['Thigh'].rotation_quaternion = randq(0, -90, -50)
            if side_name == 'rt':
                bones['Thigh'].rotation_quaternion @= randq(1, 0, 60) @ randq(2, -10, 20)
            else:
                bones['Thigh'].rotation_quaternion @= randq(1, -60, 0) @ randq(2, 0, 30)
    else:
        pass
    return bones


def randomize_arm(bones: Mapping[str, PoseBone], pose: str, side_name: str) -> Mapping[str, PoseBone]:
    bones['Clavicle'].rotation_quaternion = randq(0, -20, 0)
    bones['Clavicle'].rotation_quaternion @= randq(1) if pose == 'STAND' else randq(1, 15)
    bones['Shoulder'].rotation_quaternion = randq(0, 10, 60) @ randq(1, 40)
    bones['Bicep'].rotation_quaternion = randq(0) @ randq(1) @ randq(2)
    bones['Elbow'].rotation_quaternion = randq(0) @ randq(1)
    bones['Wrist'].rotation_quaternion = randq(0) @ randq(1) @ randq(2)
    bones['Hand'].rotation_quaternion = randq(0, 40) @ randq(1, 20) @ randq(2, 20)
    if side_name == 'lf':
        bones['Clavicle'].rotation_quaternion @= randq(2, 0, 10)
        bones['Shoulder'].rotation_quaternion @= randq(2, 0, 100)
        bones['Elbow'].rotation_quaternion @= randq(2, 0, 100)
    else:
        bones['Clavicle'].rotation_quaternion @= randq(2, -10, 0)
        bones['Shoulder'].rotation_quaternion @= randq(2, -100, 0)
        bones['Elbow'].rotation_quaternion = randq(2, -100, 0)
    return bones


def clench_finger(bones: Mapping[str, PoseBone], finger_name: str) -> Mapping[str, PoseBone]:
    bones['01'].rotation_quaternion = randq(1) @ randq(2)
    bones['02'].rotation_quaternion = randq(1) @ randq(2)
    bones['03'].rotation_quaternion = randq(1) @ randq(2)
    if finger_name == 'Index':
        bones['01'].rotation_quaternion @= randq(0, 70, 90)
        bones['02'].rotation_quaternion @= randq(0, -100, -80)
        bones['03'].rotation_quaternion @= randq(0, -10, 0)
    elif finger_name == 'Thumb':
        bones['01'].rotation_quaternion @= randq(0) @ randq(1, -25, -15)
        bones['02'].rotation_quaternion @= randq(0, 25, 35)
        bones['03'].rotation_quaternion @= randq(0, 40, 50)
    elif finger_name == 'Pinky':
        bones['01'].rotation_quaternion @= randq(0, 70, 90)
        bones['02'].rotation_quaternion @= randq(0, 90, 100)
        bones['03'].rotation_quaternion @= randq(0, 0, 10)
    else:
        bones['01'].rotation_quaternion @= randq(0, 70, 90)
        bones['02'].rotation_quaternion @= randq(0, 90, 100)
        bones['03'].rotation_quaternion @= randq(0, -10, 0)
    return bones


def curve_finger(bones: Mapping[str, PoseBone], finger_name: str) -> Mapping[str, PoseBone]:
    bones['01'].rotation_quaternion = randq(1) @ randq(2)
    bones['02'].rotation_quaternion = randq(1) @ randq(2)
    bones['03'].rotation_quaternion = randq(1) @ randq(2)
    if finger_name == 'Index':
        bones['01'].rotation_quaternion @= randq(0, 5, 45)
        bones['02'].rotation_quaternion @= randq(0, -40, -30)
        bones['03'].rotation_quaternion @= randq(0, -15, -5)
    elif finger_name == 'Thumb':
        bones['01'].rotation_quaternion @= randq(0, -20, -5) @ randq(2, 10, 20)
        bones['02'].rotation_quaternion @= randq(0)
        bones['03'].rotation_quaternion @= randq(0, -15, -5)
    elif finger_name == 'Pinky':
        bones['01'].rotation_quaternion @= randq(0, 5, 45)
        bones['02'].rotation_quaternion @= randq(0, 30, 40)
        bones['03'].rotation_quaternion @= randq(0, 5, 15)
    else:
        bones['01'].rotation_quaternion @= randq(0, 5, 45)
        bones['02'].rotation_quaternion @= randq(0, 30, 40)
        bones['03'].rotation_quaternion @= randq(0, -15, -5)
    return bones


def point_finger(bones: Mapping[str, PoseBone], finger_name: str) -> Mapping[str, PoseBone]:
    bones['01'].rotation_quaternion = randq(0, -10, -5) @ randq(1) @ randq(2)
    bones['02'].rotation_quaternion = randq(1) @ randq(2)
    bones['03'].rotation_quaternion = randq(1) @ randq(2)
    if finger_name == 'Index':
        bones['02'].rotation_quaternion @= randq(0, 10, 15)
        bones['03'].rotation_quaternion @= randq(0, 7, 12)
    elif finger_name == 'Thumb':
        bones['01'].rotation_quaternion @= randq(1, -12, -7)
        bones['02'].rotation_quaternion @= randq(0, 15, 25)
        bones['03'].rotation_quaternion @= randq(0, 7, 12)
    elif finger_name == 'Pinky':
        bones['02'].rotation_quaternion @= randq(0, -15, -10)
        bones['03'].rotation_quaternion @= randq(0, -17, -12)
    else:
        bones['02'].rotation_quaternion @= randq(0, -15, -10)
        bones['03'].rotation_quaternion @= randq(0, 7, 12)
    return bones


def randomize_finger(bones: Mapping[str, PoseBone], finger_name: str) -> Mapping[str, PoseBone]:
    return random.choice([clench_finger, curve_finger, point_finger])(bones, finger_name)


def get_bones(bones: Mapping[str, PoseBone], bone_names: Set[str], side_name: str = None,
              finger_name: str = None) -> Dict[str, PoseBone]:
    if side_name:
        if finger_name:
            if finger_name != 'Thumb':
                bone_names = {f'{side_name}Finger{finger_name}{bone_name}' for bone_name in bone_names}
            else:
                bone_names = {f'{side_name}{finger_name}{bone_name}' for bone_name in bone_names}
            return {bone_name[-2:]: bones[bone_name] for bone_name in bone_names.intersection(bones)}
        else:
            bone_names = {f'{side_name}{bone_name}' for bone_name in bone_names}
            return {bone_name[2:]: bones[bone_name] for bone_name in bone_names.intersection(bones)}
    else:
        return {bone_name: bones[bone_name] for bone_name in bone_names.intersection(bones)}


def randomize_bones(obj: Object, gender: str, pose: str) -> Object:
    bpy.ops.object.mode_set(mode='POSE')
    bones = {bone.name: bone for bone in obj.pose.bones}
    pelvis = randomize_pelvis(bones['PelvisNode'], pose, gender)
    spine = randomize_spine(get_bones(bones, {'Spine01', 'Spine02', 'Spine03', 'Spine04'}), pose, gender,
                            pelvis.rotation_quaternion)
    randomize_head(get_bones(bones, {'Neck01', 'Neck02', 'Neck03', 'Neck04', 'Head'}), gender, spine)
    leg_order = random.choice([('FORWARD', 'BACKWARD'), ('BACKWARD', 'FORWARD')])
    randomize_leg(get_bones(bones, {'Thigh', 'Calf', 'Foot'}, 'lf'), 'lf', pose, gender,
                  pelvis.rotation_quaternion.y, leg_order[0])
    randomize_leg(get_bones(bones, {'Thigh', 'Calf', 'Foot'}, 'rt'), 'rt', pose, gender,
                  pelvis.rotation_quaternion.y, leg_order[1])
    randomize_arm(get_bones(bones, {'Clavicle', 'Shoulder', 'Bicep', 'Elbow', 'Wrist', 'Hand'}, 'lf'), pose, 'lf')
    randomize_arm(get_bones(bones, {'Clavicle', 'Shoulder', 'Bicep', 'Elbow', 'Wrist', 'Hand'}, 'rt'), pose, 'rt')
    fingers = {'Index', 'Middle', 'Ring', 'Pinky', 'Thumb'}
    for finger in fingers:
        randomize_finger(get_bones(bones, {'01', '02', '03'}, 'lf', finger), finger)
        randomize_finger(get_bones(bones, {'01', '02', '03'}, 'rt', finger), finger)
    return obj
