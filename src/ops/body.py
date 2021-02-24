import bpy
from ..avi.proxy_group import ProxyGroup


class MaleBody(bpy.types.Operator):
    """Add default IMVU male body"""
    bl_idname = "mesh.primitive_imvu_male_body_add"
    bl_label = "Body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        head_prox = ("MHead", "head.pickle")
        torso_prox = ("MTorso", "torso.pickle")
        hands_prox = ("MHands", "hands.pickle")
        legs_prox = ("MLegs", "legs.pickle")
        calfs_prox = ("MCalfs", "calfs.pickle")
        feet_prox = ("MFeet", "feet.pickle")
        mesh_group = ProxyGroup(head_prox, torso_prox, hands_prox,
                                legs_prox, calfs_prox, feet_prox)
        mesh_group.to_mesh("MBody")
        return {'FINISHED'}
