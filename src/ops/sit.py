import bpy
from ..node.pose import Pose


class SittingSpot(bpy.types.Operator):
    """Add an imvu sitting spot to the scene"""
    bl_idname = "object.empty_imvu_sit_add"
    bl_label = "Sit"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    def execute(self, context):
        sit_pose = Pose('Sit', context)
        sit_pose.to_scene()
        return {'FINISHED'}
