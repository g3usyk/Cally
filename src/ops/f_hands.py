import bpy
from ..avi.proxy import Proxy


class FemaleHands(bpy.types.Operator):
    """Add default IMVU female hands"""
    bl_idname = "mesh.primitive_imvu_female_hands_add"
    bl_label = "Hands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("FHands", ["assets", "female", "hands.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
