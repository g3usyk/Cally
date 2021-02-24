import bpy
from ..avi.proxy import Proxy


class MaleHands(bpy.types.Operator):
    """Add default IMVU male hands"""
    bl_idname = "mesh.primitive_imvu_male_hands_add"
    bl_label = "Hands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("MHands", "hands.pickle")
        mesh.to_mesh()
        return {'FINISHED'}
