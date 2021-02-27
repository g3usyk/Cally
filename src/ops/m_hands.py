import bpy
from ..avi.proxy import Proxy


class MaleHands(bpy.types.Operator):
    """Adds imvu mesh primitive male hands to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_hands_add"
    bl_label = "Hands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Hands", ["assets", "male", "hands.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
