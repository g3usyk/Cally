import bpy
from ..body_part import BodyPart


class FemaleLegs(bpy.types.Operator):
    """Adds imvu mesh primitive female legs to scene"""
    part = BodyPart("female", "legs")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

    def execute(self, context):
        return self.part.execute(context)
