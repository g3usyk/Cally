from bpy.types import Context, Operator
from bpy.props import EnumProperty
from typing import Set
from ..node.pose import Pose


class SittingSpot(Operator):
    """Add an imvu sitting spot to the scene"""
    bl_idname = "object.empty_imvu_sit_add"
    bl_label = "Sit"
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

    def execute(self, context: Context) -> Set[str]:
        sit_pose = Pose('Sit', context)
        sit_pose.to_scene(self.primitive)
        return {'FINISHED'}
