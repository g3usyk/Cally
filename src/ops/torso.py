import bpy
from ..avi.male import torso as mtorso


class MaleTorso(bpy.types.Operator):
    '''Add default IMVU male torso'''
    bl_idname = "mesh.primitive_imvu_male_torso_add"
    bl_label = "Torso"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mtorso.Torso()
        mesh.to_mesh("MTorso")
        return {'FINISHED'}
