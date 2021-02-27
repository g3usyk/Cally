import bpy

from .arm.master_root import add_master_root


class DefaultSkeleton(bpy.types.Operator):
    """Adds default imvu armature to scene.

    """
    bl_idname = "object.armature_imvu_skeleton_add"
    bl_label = "IMVU Master Root"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Calls armature generation method.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:
            A dictionary containing the success state of the method.

        """
        add_master_root()
        return {'FINISHED'}
