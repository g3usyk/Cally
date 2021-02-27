import bpy
from ..avi.proxy import Proxy


class FemaleFeet(bpy.types.Operator):
    """Adds imvu mesh primitive female feet to scene.

    """
    bl_idname = "mesh.primitive_imvu_female_feet_add"
    bl_label = "Feet"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("F.Feet", ["assets", "female", "feet.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
