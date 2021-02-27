import bpy
from ..avi.proxy import Proxy


class MaleHead(bpy.types.Operator):
    """Adds imvu mesh primitive male head to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_head_add"
    bl_label = "Head"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Head", ["assets", "male", "head.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
