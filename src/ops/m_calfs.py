import bpy
from ..avi.proxy import Proxy


class MaleCalfs(bpy.types.Operator):
    """Adds imvu mesh primitive male calves to scene.

    """
    bl_idname = "mesh.primitive_imvu_male_calfs_add"
    bl_label = "Calfs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("M.Calfs", ["assets", "male", "calfs.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
