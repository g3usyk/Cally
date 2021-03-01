import bpy


class Pose:

    def __init__(self, pose_type):
        self.pose_type = pose_type
        pass

    def to_scene(self):
        bpy.ops.object.empty_add(type='SPHERE')
        node = bpy.context.active_object
        node.name = 'Node'
        bpy.context.object.empty_display_size = 0.20
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        spot = bpy.context.active_object
        spot.name = f'Spot.{self.pose_type}'
        spot.parent = node
