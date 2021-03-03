import bpy
from bpy.props import (
    BoolProperty,
)
from ..body_part import BodyPart


class MaleTorso(bpy.types.Operator):
    """Add imvu mesh primitive male torso to scene"""
    part = BodyPart("male", "torso")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

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
        self.part.uvs = self.uv
        return self.part.execute(context)
