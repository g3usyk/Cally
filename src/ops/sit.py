import bpy
from ..node.pose import Pose


class SittingSpot(bpy.types.Operator):
    """Add an imvu sitting spot to the scene"""
    bl_idname = "object.empty_imvu_sit_add"
    bl_label = "Sit"

    def execute(self, context):
        p = Pose('Sitting')
        p.to_scene()
        return {'FINISHED'}
