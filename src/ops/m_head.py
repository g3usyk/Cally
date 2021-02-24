import bpy
from ..avi.proxy import Proxy


class MaleHead(bpy.types.Operator):
    """Add default IMVU male head"""
    bl_idname = "mesh.primitive_imvu_male_head_add"
    bl_label = "Head"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("MHead", ["assets", "male", "head.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
