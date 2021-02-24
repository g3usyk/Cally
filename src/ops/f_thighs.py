import bpy
from ..avi.proxy import Proxy


class FemaleThighs(bpy.types.Operator):
    """Add default IMVU female thighs"""
    bl_idname = "mesh.primitive_imvu_female_thighs_add"
    bl_label = "Thighs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("F.Thighs", ["assets", "female", "thighs.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
