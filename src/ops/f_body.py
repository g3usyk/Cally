import bpy
from ..avi.proxy_group import ProxyGroup


class FemaleBody(bpy.types.Operator):
    """Adds imvu mesh primitive female body parts to scene.

    """
    bl_idname = "mesh.primitive_imvu_female_body_add"
    bl_label = "Body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Generates mesh data for each female body part under a new collection.

        Args:
            context (): A bpy context containing data in the current 3D View.

        Returns:
            A dictionary containing the success state of the method.

        """
        head_prox = ("F.Head", ["assets", "female", "head.pickle"])
        torso_prox = ("F.Torso", ["assets", "female", "torso.pickle"])
        hands_prox = ("F.Hands", ["assets", "female", "hands.pickle"])
        legs_prox = ("F.Legs", ["assets", "female", "legs.pickle"])
        thighs_prox = ("F.Thighs", ["assets", "female", "thighs.pickle"])
        feet_prox = ("F.Feet", ["assets", "female", "feet.pickle"])
        mesh_group = ProxyGroup(head_prox, torso_prox, hands_prox,
                                legs_prox, thighs_prox, feet_prox)
        mesh_group.to_mesh("FBody")
        return {'FINISHED'}
