from typing import AbstractSet


class GroupMap:
    mapping = {'pelvis': {'PelvisNode'},
               'l_leg': {'lfCalf', 'lfHip', 'lfFoot', 'lfThigh', 'lfToes'},
               'r_leg': {'rtThigh', 'rtCalf', 'rtHip', 'rtFoot', 'rtToes'},
               'spine': {'Spine03', 'Spine01', 'Spine02', 'Spine04'},
               'head': {'Neck01', 'Neck02', 'Neck04', 'Head', 'Neck03'},
               'l_arm': {'lfShoulder', 'lfBicep', 'lfWrist', 'lfElbow', 'lfClavicle'},
               'l_hand': {'lfFingerRing02', 'lfFingerIndex02', 'lfFingerIndex03', 'lfThumb01', 'lfmetaCarpal01',
                          'lfFingerPinky01', 'lfmetaCarpal04', 'lfmetaCarpal05', 'lfmetaCarpal02', 'lfFingerRing03',
                          'lfFingerMiddle03', 'lfFingerMiddle02', 'lfThumb03', 'lfFingerPinky02', 'lfFingerPinky03',
                          'lfFingerRing01', 'lfHand', 'lfFingerMiddle01', 'lfmetaCarpal03', 'lfFingerIndex01',
                          'lfThumb02'},
               'r_arm': {'rtBicep', 'rtElbow', 'rtClavicle', 'rtShoulder', 'rtWrist'},
               'r_hand': {'rtFingerIndex02', 'rtThumb01', 'rtFingerPinky02', 'rtFingerPinky01', 'rtFingerIndex03',
                          'rtFingerRing01', 'rtFingerRing02', 'rtFingerMiddle01', 'rtmetaCarpal04', 'rtmetaCarpal01',
                          'rtHand', 'rtmetaCarpal05', 'rtFingerPinky03', 'rtmetaCarpal02', 'rtFingerRing03',
                          'rtmetaCarpal03', 'rtThumb02', 'rtFingerIndex01', 'rtFingerMiddle02', 'rtFingerMiddle03',
                          'rtThumb03'}
               }

    @classmethod
    def lookup(cls, bone_group: str) -> AbstractSet[str]:
        return cls.mapping[bone_group]
