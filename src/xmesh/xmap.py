import math

class WeightMap():
    """Default weights for imvu base male avatar"""
    wmap = {}

    wmap["Female03MasterRoot"] = 0
    wmap["PelvisNode"] = 1
    wmap["lfHip"] = 2
    wmap["lfThigh"] = 3
    wmap["lfCalf"] = 4
    wmap["lfFoot"] = 5
    wmap["lfToes"] = 6
    wmap["rtHip"] = 8
    wmap["rtThigh"] = 9
    wmap["rtCalf"] = 10
    wmap["rtFoot"] = 11
    wmap["rtToes"] = 12
    wmap["Spine01"] = 14
    wmap["Spine02"] = 15
    wmap["Spine03"] = 16
    wmap["Spine04"] = 17
    wmap["Neck01"] = 18
    wmap["Neck02"] = 19
    wmap["Neck03"] = 20
    wmap["Neck04"] = 21
    wmap["Head"] = 22
    wmap["lfClavicle"] = 24
    wmap["lfShoulder"] = 25
    wmap["lfBicep"] = 26
    wmap["lfElbow"] = 27
    wmap["lfWrist"] = 28
    wmap["lfHand"] = 29
    wmap["lfmetaCarpal03"] = 30
    wmap["lfFingerMiddle01"] = 31
    wmap["lfFingerMiddle02"] = 32
    wmap["lfFingerMiddle03"] = 33
    wmap["lfmetaCarpal01"] = 35
    wmap["lfThumb01"] = 36
    wmap["lfThumb02"] = 37
    wmap["lfThumb03"] = 38
    wmap["lfmetaCarpal05"] = 40
    wmap["lfFingerPinky01"] = 41
    wmap["lfFingerPinky02"] = 42
    wmap["lfFingerPinky03"] = 43
    wmap["lfmetaCarpal02"] = 45
    wmap["lfFingerIndex01"] = 46
    wmap["lfFingerIndex02"] = 47
    wmap["lfFingerIndex03"] = 48
    wmap["lfmetaCarpal04"] = 50
    wmap["lfFingerRing01"] = 51
    wmap["lfFingerRing02"] = 52
    wmap["lfFingerRing03"] = 53
    wmap["rtClavicle"] = 55
    wmap["rtShoulder"] = 56
    wmap["rtBicep"] = 57
    wmap["rtElbow"] = 58
    wmap["rtWrist"] = 59
    wmap["rtHand"] = 60
    wmap["rtmetaCarpal03"] = 61
    wmap["rtFingerMiddle01"] = 62
    wmap["rtFingerMiddle02"] = 63
    wmap["rtFingerMiddle03"] = 64
    wmap["rtmetaCarpal01"] = 66
    wmap["rtThumb01"] = 67
    wmap["rtThumb02"] = 68
    wmap["rtThumb03"] = 69
    wmap["rtmetaCarpal05"] = 71
    wmap["rtFingerPinky01"] = 72
    wmap["rtFingerPinky02"] = 73
    wmap["rtFingerPinky03"] = 74
    wmap["rtmetaCarpal02"] = 76
    wmap["rtFingerIndex01"] = 77
    wmap["rtFingerIndex02"] = 78
    wmap["rtFingerIndex03"] = 79
    wmap["rtmetaCarpal04"] = 81
    wmap["rtFingerRing01"] = 82
    wmap["rtFingerRing02"] = 83
    wmap["rtFingerRing03"] = 84

    @classmethod
    def lookup(cls, bone):
        return cls.wmap[bone]

