import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)
from ..node.pose import Pose

curr_axis = {'x'}


class SittingSpot(bpy.types.Operator):
    """Add an imvu sitting spot to the scene"""
    bl_idname = "object.empty_imvu_sit_add"
    bl_label = "Sit"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    array: BoolProperty(
        name="Array",
        description="Repeats node along array",
        default=False,
    )

    count: IntProperty(
        name="Count",
        description="Count of nodes in array",
        default=1,
        min=1,
        soft_max=10,
    )

    def update_axis(self, context):
        global curr_axis
        if len(self.axis) == 0 or len(self.axis) > 1:
            self.axis = curr_axis
        curr_axis = self.axis

    axis: EnumProperty(
        name="Axis",
        description="Axis for array",
        options={"ENUM_FLAG"},
        items=(
            ('x', 'X', ''),
            ('y', 'Y', ''),
            ('z', 'Z', ''),
        ),
        default=curr_axis,
        update=update_axis,
    )

    offset: FloatProperty(
        name="Offset",
        description="Offset distance between each node",
        soft_min=-100.0,
        soft_max=100.0,
        default=2.0,
        step=1,
    )

    def execute(self, context):
        p = Pose('Sitting')
        ax = next(iter(self.axis))
        if self.array:
            head = p.to_scene()
            for i in range(1, self.count):
                amt = i * self.offset
                if ax == 'x':
                    p.to_scene(loc=(amt, 0, 0), parent=head)
                elif ax == 'y':
                    p.to_scene(loc=(0, amt, 0), parent=head)
                else:
                    p.to_scene(loc=(0, 0, amt), parent=head)
        else:
            p.to_scene()
        return {'FINISHED'}
