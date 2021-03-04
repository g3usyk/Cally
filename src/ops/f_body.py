import bpy
from bpy.props import (
    BoolProperty,
)
from .body_group import BodyGroup


class FemaleBody(bpy.types.Operator):
    """Add imvu mesh primitive female body parts to scene"""
    group = BodyGroup("female", ["head", "torso", "hands", "thighs", "legs", "feet"])
    bl_idname = group.bl_idname
    bl_label = group.bl_label
    bl_options = group.bl_options

    head: BoolProperty(
        name="Head",
        description="Include head for the newly added collection",
        default=True,
    )

    torso: BoolProperty(
        name="Torso",
        description="Include torso for the newly added collection",
        default=True,
    )

    hands: BoolProperty(
        name="Hands",
        description="Include hands for the newly added collection",
        default=True,
    )

    thighs: BoolProperty(
        name="Thighs",
        description="Include thighs for the newly added collection",
        default=True,
    )

    legs: BoolProperty(
        name="Legs",
        description="Include legs for the newly added collection",
        default=True,
    )

    feet: BoolProperty(
        name="Feet",
        description="Include feet for the newly added collection",
        default=True,
    )

    uv: BoolProperty(
        name="UVs",
        description="Generate uv coordinates",
        default=True,
    )

    weight: BoolProperty(
        name="Vertex Groups",
        description="Include automatic bone weight assignments",
        default=True
    )

    def execute(self, context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context ():  A bpy context containing data in the current 3d view.

        Returns:

        """
        self.group.uvs = self.uv
        self.group.weights = self.weight
        return self.group.execute([self.head, self.torso, self.hands, self.thighs, self.legs, self.feet])
