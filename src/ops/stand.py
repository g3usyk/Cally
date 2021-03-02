import bpy
from ..node.pose import Pose


class StandingSpot(bpy.types.Operator):
    """Add an imvu standing spot to the scene"""
    bl_idname = "object.empty_imvu_stand_add"
    bl_label = "Stand"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        p = Pose('Standing')
        p.to_scene()
        return {'FINISHED'}
