import bpy

from bpy.props import BoolProperty

from .body_group import BodyGroup


class MaleBody(bpy.types.Operator):
    """Add imvu mesh primitive male body parts to scene"""
    group = BodyGroup("male", [("head", "eyes", "brows", "lashes"), "torso", "hands", "legs", "calfs", "feet"])
    bl_idname = group.bl_idname
    bl_label = group.bl_label
    bl_options = group.bl_options

    head: BoolProperty(
        name="Head",
        description="Include head in the newly added collection",
        default=True,
    )

    torso: BoolProperty(
        name="Torso",
        description="Include torso in the newly added collection",
        default=True,
    )

    hands: BoolProperty(
        name="Hands",
        description="Include hands in the newly added collection",
        default=True,
    )

    legs: BoolProperty(
        name="Legs",
        description="Include legs in the newly added collection",
        default=True,
    )

    calfs: BoolProperty(
        name="Calfs",
        description="Include calves in the newly added collection",
        default=True,
    )

    feet: BoolProperty(
        name="Feet",
        description="Include feet in the newly added collection",
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

    morph: BoolProperty(
        name="Morphs",
        description="Include shape key morphs",
        default=True
    )

    def execute(self, context: bpy.types.Context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context (bpy.types.Context): The context containing data for the current 3d view.

        Returns:

        """
        self.group.uvs = self.uv
        self.group.weights = self.weight
        return self.group.execute([self.head, self.torso, self.hands, self.legs, self.calfs, self.feet])
