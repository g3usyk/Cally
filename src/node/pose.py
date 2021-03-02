import bpy


class Pose:

    def __init__(self, pose_type):
        self.pose_type = pose_type
        pass

    def to_scene(self, loc=None, parent=None):
        if loc is None:
            bpy.ops.object.empty_add(type='SPHERE')
        else:
            bpy.ops.object.empty_add(type='SPHERE', location=loc)
        node = bpy.context.active_object
        node.name = 'Node'
        if parent is not None:
            node.parent = parent
        bpy.context.object.empty_display_size = 0.20
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        spot = bpy.context.active_object
        spot.name = f'Spot.{self.pose_type}'
        spot.parent = node
        return node
