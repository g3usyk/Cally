import bpy
from ..body_group import BodyGroup


class FemaleBody(bpy.types.Operator):
    """Adds imvu mesh primitive female body parts to scene"""
    group = BodyGroup("female", ["feet", "hands", "head", "legs", "thighs", "torso"])
    bl_idname = group.bl_idname
    bl_label = group.bl_label
    bl_options = group.bl_options

    def execute(self, context):
        return self.group.execute(context)
