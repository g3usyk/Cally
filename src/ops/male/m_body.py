import bpy
from bpy.props import (
    BoolProperty,
)
from ..body_group import BodyGroup


class MaleBody(bpy.types.Operator):
    """Add imvu mesh primitive male body parts to scene"""
    group = BodyGroup("male", ["feet", "hands", "head", "legs", "calfs", "torso"])
    bl_idname = group.bl_idname
    bl_label = group.bl_label
    bl_options = group.bl_options

    uv: BoolProperty(
        name="Add UVs",
        description="Generate uv coordinates",
        default=True,
    )

    def execute(self, context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:

        """
        self.group.uvs = self.uv
        return self.group.execute(context)
