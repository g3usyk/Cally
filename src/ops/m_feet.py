import bpy
from ..avi.proxy import Proxy


class MaleFeet(bpy.types.Operator):
    """Adds imvu mesh primitive male feet to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_feet_add"
    bl_label = "Feet"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Feet", ["assets", "male", "feet.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
