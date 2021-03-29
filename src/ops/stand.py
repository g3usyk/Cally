import bpy

from bpy.props import EnumProperty

from ..node.pose import Pose


class StandingSpot(bpy.types.Operator):
    """Add an imvu standing spot to the scene"""
    bl_idname = "object.empty_imvu_stand_add"
    bl_label = "Stand"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    primitive: EnumProperty(
        name="Display",
        description="Object display type",
        items=(
            ('ARROWS', 'Arrows', 'Empty arrows'),
            ('PLAIN_AXES', 'Axes', 'Empty axes')
        ),
        default="ARROWS",
    )

    def execute(self, context: bpy.types.Context):
        stand_pose = Pose('Stand', context)
        stand_pose.to_scene(self.primitive)
        return {'FINISHED'}
