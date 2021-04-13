import random
from typing import Set

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from bpy.types import Context, Operator

from ..arm.master_root import add_master_root, link_body, lock_bones
from ..arm.randomize import randomize_bones


class DefaultSkeleton(Operator):
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

    link: BoolProperty(
        name="Link",
        description="Include linked avatar mesh",
        default=False
    )

    display: EnumProperty(
        name="Display As",
        description="Display bones as specified shape",
        items=(
            ('OCTAHEDRAL', 'Octahedral', 'Display bones as octahedral shape'),
            ('STICK', 'Stick', 'Display bones as simple 2D lines with dots'),
            ('BBONE', 'B-Bone', 'Display bones as boxes, showing subdivision and B-Splines'),
            ('ENVELOPE', 'Envelope', 'Display bones as extruded spheres, showing deformation influence volume'),
            ('WIRE', 'Wire', 'Display bones as thin wires, showing subdivision and B-Splines'),
        ),
        default="OCTAHEDRAL"
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

    def execute(self, context: Context) -> Set[str]:
        """Calls armature generation method.

        Args:
            context (bpy.types.Context): The context containing data for the current 3d view.

        Returns:
            A set containing the success state of the method.

        """
        armature = add_master_root()
        armature.data.display_type = self.display
        if self.randomize != 0:
            randomize_bones(armature, self.gender, self.pose)
        link_body(context, armature, self.gender) if self.link else None
        lock_bones(armature) if self.lock else None
        return {'FINISHED'}

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.prop(self, 'lock')
        row.prop(self, 'link')
        layout.prop(self, 'display')
        layout.prop(self, 'gender')
        layout.prop(self, 'randomize')
        layout.prop(self, 'pose')
