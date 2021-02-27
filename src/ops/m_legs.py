import bpy
from ..avi.proxy import Proxy


class MaleLegs(bpy.types.Operator):
    """Adds imvu mesh primitive male legs to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_legs_add"
    bl_label = "Legs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Legs", ["assets", "male", "legs.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
