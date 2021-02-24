import bpy
from ..avi.proxy_group import ProxyGroup


class MaleBody(bpy.types.Operator):
    """Add default IMVU male body"""
    bl_idname = "mesh.primitive_imvu_male_body_add"
    bl_label = "Body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        head_prox = ("MHead", ["assets", "male", "head.pickle"])
        torso_prox = ("MTorso", ["assets", "male", "torso.pickle"])
        hands_prox = ("MHands", ["assets", "male", "hands.pickle"])
        legs_prox = ("MLegs", ["assets", "male", "legs.pickle"])
        calfs_prox = ("MCalfs", ["assets", "male", "calfs.pickle"])
        feet_prox = ("MFeet", ["assets", "male", "feet.pickle"])
        mesh_group = ProxyGroup(head_prox, torso_prox, hands_prox,
                                legs_prox, calfs_prox, feet_prox)
        mesh_group.to_mesh("MBody")
        return {'FINISHED'}
