import bpy
from ..avi.proxy import Proxy


class MaleFeet(bpy.types.Operator):
    """Add default IMVU male feet"""
    bl_idname = "mesh.primitive_imvu_male_feet_add"
    bl_label = "Feet"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("MFeet", ["assets", "male", "feet.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
