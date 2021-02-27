import bpy
from ..avi.proxy import Proxy


class FemaleHands(bpy.types.Operator):
    """Adds imvu mesh primitive female hands to scene.

    """
    bl_idname = "mesh.primitive_imvu_female_hands_add"
    bl_label = "Hands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("F.Hands", ["assets", "female", "hands.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
