import bpy
import random

from bpy.props import BoolProperty, EnumProperty, FloatProperty

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

    randomize: FloatProperty(
        name="Random",
        description="Random seed value",
    )

    gender: EnumProperty(
        name="Gender",
        description="Gender type for randomizer",
        items=(
            ('MALE', 'Male', 'Male skeleton'),
            ('FEMALE', 'Female', 'Female Skeleton')
        ),
        default='MALE'
    )

    pose: EnumProperty(
        name="Pose",
        description="Pose type for randomizer",
        items=(
            ('STAND', 'Stand', 'Standing pose'),
            ('SIT', 'Sit', 'Sitting pose')
        ),
        default='STAND'
    )

    def execute(self, context: bpy.types.Context):
        """Calls armature generation method.

        Args:
            context (bpy.types.Context): The context containing data for the current 3d view.

        Returns:
            A set containing the success state of the method.

        """
        bones = add_master_root()
        if self.randomize != 0:
            randomize_bones(bones, self.gender, self.pose)
        if self.lock:
            lock_bones(bones)
        return {'FINISHED'}
