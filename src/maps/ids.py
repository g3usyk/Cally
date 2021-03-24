class IDMap:
    mapping = {"Female03MasterRoot": 0,
               "PelvisNode": 1,
               "lfHip": 2,
               "lfThigh": 3,
               "lfCalf": 4,
               "lfFoot": 5,
               "lfToes": 6,

               "rtHip": 8,
               "rtThigh": 9,
               "rtCalf": 10,
               "rtFoot": 11,
               "rtToes": 12,

               "Spine01": 14,
               "Spine02": 15,
               "Spine03": 16,
               "Spine04": 17,

               "Neck01": 18,
               "Neck02": 19,
               "Neck03": 20,
               "Neck04": 21,
               "Head": 22,

               "lfClavicle": 24,
               "lfShoulder": 25,
               "lfBicep": 26,
               "lfElbow": 27,
               "lfWrist": 28,
               "lfHand": 29,

               "lfmetaCarpal03": 30,
               "lfFingerMiddle01": 31,
               "lfFingerMiddle02": 32,
               "lfFingerMiddle03": 33,

               "lfmetaCarpal01": 35,
               "lfThumb01": 36,
               "lfThumb02": 37,
               "lfThumb03": 38,
               "lfmetaCarpal05": 40,

               "lfFingerPinky01": 41,
               "lfFingerPinky02": 42,
               "lfFingerPinky03": 43,
               "lfmetaCarpal02": 45,

               "lfFingerIndex01": 46,
               "lfFingerIndex02": 47,
               "lfFingerIndex03": 48,
               "lfmetaCarpal04": 50,

               "lfFingerRing01": 51,
               "lfFingerRing02": 52,
               "lfFingerRing03": 53,
               "rtClavicle": 55,
               "rtShoulder": 56,

               "rtBicep": 57,
               "rtElbow": 58,
               "rtWrist": 59,
               "rtHand": 60,
               "rtmetaCarpal03": 61,
               "rtFingerMiddle01": 62,

               "rtFingerMiddle02": 63,
               "rtFingerMiddle03": 64,
               "rtmetaCarpal01": 66,
               "rtThumb01": 67,
               "rtThumb02": 68,

               "rtThumb03": 69,
               "rtmetaCarpal05": 71,
               "rtFingerPinky01": 72,
               "rtFingerPinky02": 73,
               "rtFingerPinky03": 74,

               "rtmetaCarpal02": 76,
               "rtFingerIndex01": 77,
               "rtFingerIndex02": 78,
               "rtFingerIndex03": 79,

               "rtmetaCarpal04": 81,
               "rtFingerRing01": 82,
               "rtFingerRing02": 83,
               "rtFingerRing03": 84}

    @classmethod
    def lookup(cls, bone_name: str) -> int:
        return cls.mapping[bone_name]
