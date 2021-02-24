import bpy
from ..avi.male import hands as mhands


class MaleHands(bpy.types.Operator):
    '''Add default IMVU male hands'''
    bl_idname = "mesh.primitive_imvu_male_hands_add"
    bl_label = "Hands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mhands.Hands()
        mesh.to_mesh("MHands")
        return {'FINISHED'}
