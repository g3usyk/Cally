import bpy
from ..avi.male import legs as mlegs


class MaleLegs(bpy.types.Operator):
    '''Add default IMVU male legs'''
    bl_idname = "mesh.primitive_imvu_male_legs_add"
    bl_label = "Legs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mlegs.Legs()
        mesh.to_mesh("MLegs")
        return {'FINISHED'}
