import bpy
from ..avi.proxy import Proxy


class MaleCalfs(bpy.types.Operator):
    """Add default IMVU male calves"""
    bl_idname = "mesh.primitive_imvu_male_calfs_add"
    bl_label = "Calfs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("M.Calfs", ["assets", "male", "calfs.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
