import bpy
from ..body_part import BodyPart


class MaleLegs(bpy.types.Operator):
    """Adds imvu mesh primitive male legs to scene"""
    part = BodyPart("male", "legs")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

    def execute(self, context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:

        """
        return self.part.execute(context)
