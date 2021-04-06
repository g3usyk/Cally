import bpy
import random

from bpy.props import BoolProperty, FloatProperty

from ..arm.master_root import add_master_root, lock_bones, randomize_bones


class DefaultSkeleton(bpy.types.Operator):
    """Add default imvu armature to the scene"""
    bl_idname = "object.armature_imvu_bones_add"
    bl_label = "Bones"
    bl_options = {'REGISTER', 'UNDO'}
    current_offset = random.random()

    lock: BoolProperty(
        name="Lock",
        description="Use default transformation locks on each bone",
        default=True,
    )

    seed: FloatProperty(
        name="Seed",
        description="Random seed value",
    )

    def execute(self, context: bpy.types.Context):
        """Calls armature generation method.

        Args:
            context (bpy.types.Context): The context containing data for the current 3d view.

        Returns:
            A set containing the success state of the method.

        """
        bones = add_master_root()
        if self.seed != 0:
            randomize_bones(bones)
        if self.lock:
            lock_bones(bones)
        return {'FINISHED'}
