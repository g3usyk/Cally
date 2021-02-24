import bpy
from ..avi.proxy import Proxy


class FemaleTorso(bpy.types.Operator):
    """Add default IMVU female torso"""
    bl_idname = "mesh.primitive_imvu_female_torso_add"
    bl_label = "Torso"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("F.Torso", ["assets", "female", "torso.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
