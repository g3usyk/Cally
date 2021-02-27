import bpy
from ..body_part import BodyPart


class FemaleTorso(bpy.types.Operator):
    """Adds imvu mesh primitive female torso to scene"""
    part = BodyPart("female", "torso")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

    def execute(self, context):
        return self.part.execute(context)
