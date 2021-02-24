import bpy
from ..avi.proxy_group import ProxyGroup


class FemaleBody(bpy.types.Operator):
    """Add default IMVU female body"""
    bl_idname = "mesh.primitive_imvu_female_body_add"
    bl_label = "Body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        head_prox = ("FHead", ["assets", "female", "head.pickle"])
        torso_prox = ("FTorso", ["assets", "female", "torso.pickle"])
        hands_prox = ("FHands", ["assets", "female", "hands.pickle"])
        legs_prox = ("FLegs", ["assets", "female", "legs.pickle"])
        thighs_prox = ("FThighs", ["assets", "female", "thighs.pickle"])
        feet_prox = ("FFeet", ["assets", "female", "feet.pickle"])
        mesh_group = ProxyGroup(head_prox, torso_prox, hands_prox,
                                legs_prox, thighs_prox, feet_prox)
        mesh_group.to_mesh("FBody")
        return {'FINISHED'}
