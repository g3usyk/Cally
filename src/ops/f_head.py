import bpy
from ..avi.proxy import Proxy


class FemaleHead(bpy.types.Operator):
    """Add default IMVU female head"""
    bl_idname = "mesh.primitive_imvu_female_head_add"
    bl_label = "Head"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("F.Head", ["assets", "female", "head.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
