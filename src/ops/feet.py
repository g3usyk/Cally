import bpy
from ..avi.male import feet as mfeet


class MaleFeet(bpy.types.Operator):
    '''Add default IMVU male feet'''
    bl_idname = "mesh.primitive_imvu_male_feet_add"
    bl_label = "Feet"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mfeet.Feet()
        mesh.to_mesh("MFeet")
        return {'FINISHED'}
