import bpy
from ..avi.proxy import Proxy


class MaleTorso(bpy.types.Operator):
    """Adds imvu mesh primitive male torso to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_torso_add"
    bl_label = "Torso"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Torso", ["assets", "male", "torso.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
