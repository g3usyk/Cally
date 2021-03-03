import bpy

from ..arm.master_root import add_master_root


class DefaultSkeleton(bpy.types.Operator):
    """Add default imvu armature to the scene"""
    bl_idname = "object.armature_imvu_bones_add"
    bl_label = "Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Calls armature generation method.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:
            A set containing the success state of the method.

        """
        add_master_root()
        return {'FINISHED'}
