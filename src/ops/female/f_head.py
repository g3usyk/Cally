import bpy
from ..body_part import BodyPart


class FemaleHead(bpy.types.Operator):
    """Adds imvu mesh primitive female head to scene"""
    part = BodyPart("female", "head")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

    def execute(self, context):
        return self.part.execute(context)
