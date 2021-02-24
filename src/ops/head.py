import bpy
from ..avi.male import head as mhead


class MaleHead(bpy.types.Operator):
    '''Add default IMVU male head'''
    bl_idname = "mesh.primitive_imvu_male_head_add"
    bl_label = "Head"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mhead.Head()
        mesh.to_mesh("MHead")
        return {'FINISHED'}
