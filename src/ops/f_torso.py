import bpy
from ..avi.proxy import Proxy


class FemaleTorso(bpy.types.Operator):
    """Adds imvu mesh primitive female torso to scene.

    """
    bl_idname = "mesh.primitive_imvu_female_torso_add"
    bl_label = "Torso"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data from binary data file.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        mesh = Proxy("F.Torso", ["assets", "female", "torso.pickle"])
        mesh.to_mesh()
        return {'FINISHED'}
