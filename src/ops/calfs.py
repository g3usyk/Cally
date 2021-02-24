import bpy
from ..avi.male import calfs as mcalfs


class MaleCalfs(bpy.types.Operator):
    '''Add default IMVU male calves'''
    bl_idname = "mesh.primitive_imvu_male_calfs_add"
    bl_label = "Calfs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = mcalfs.Calfs()
        mesh.to_mesh("MCalfs")
        return {'FINISHED'}
