import bpy
from ..avi.proxy_group import ProxyGroup


class MaleBody(bpy.types.Operator):
    """Add default IMVU male body"""
    bl_idname = "mesh.primitive_imvu_male_body_add"
    bl_label = "Body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        head_prox = ("M.Head", ["assets", "male", "head.pickle"])
        torso_prox = ("M.Torso", ["assets", "male", "torso.pickle"])
        hands_prox = ("M.Hands", ["assets", "male", "hands.pickle"])
        legs_prox = ("M.Legs", ["assets", "male", "legs.pickle"])
        calfs_prox = ("M.Calfs", ["assets", "male", "calfs.pickle"])
        feet_prox = ("M.Feet", ["assets", "male", "feet.pickle"])
        mesh_group = ProxyGroup(head_prox, torso_prox, hands_prox,
                                legs_prox, calfs_prox, feet_prox)
        mesh_group.to_mesh("MBody")
        return {'FINISHED'}
