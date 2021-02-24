import bpy
from ..avi.proxy import Proxy


class FemaleFeet(bpy.types.Operator):
    """Add default IMVU female feet"""
    bl_idname = "mesh.primitive_imvu_female_feet_add"
    bl_label = "Feet"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("F.Feet", ["assets", "female", "feet.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
