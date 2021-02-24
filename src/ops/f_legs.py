import bpy
from ..avi.proxy import Proxy


class FemaleLegs(bpy.types.Operator):
    """Add default IMVU female legs"""
    bl_idname = "mesh.primitive_imvu_female_legs_add"
    bl_label = "Legs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("FLegs", ["assets", "female", "legs.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
