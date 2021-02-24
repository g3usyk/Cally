import bpy

from .arm.master_root import add_master_root


class DefaultSkeleton(bpy.types.Operator):
    """Add default IMVU armature"""
    bl_idname = "object.armature_imvu_skeleton_add"
    bl_label = "IMVU Master Root"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_master_root()
        return {'FINISHED'}
