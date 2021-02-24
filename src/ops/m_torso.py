import bpy
from ..avi.proxy import Proxy


class MaleTorso(bpy.types.Operator):
    """Add default IMVU male torso"""
    bl_idname = "mesh.primitive_imvu_male_torso_add"
    bl_label = "Torso"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy("M.Torso", ["assets", "male", "torso.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
