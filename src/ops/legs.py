import bpy
from ..avi.proxy import Proxy


class MaleLegs(bpy.types.Operator):
    """Add default IMVU male legs"""
    bl_idname = "mesh.primitive_imvu_male_legs_add"
    bl_label = "Legs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("MLegs", "legs.pickle")
        mesh.to_mesh()
        return {'FINISHED'}
