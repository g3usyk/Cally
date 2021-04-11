from bpy.types import Context, Menu


class VIEW3D_MT_imvu(Menu):
    """Outlines menu layout for imvu submenus.

    """
    bl_idname = "VIEW3D_MT_imvu"
    bl_label = "IMVU"

    def draw(self, context: Context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("object.armature_imvu_bones_add", icon="BONE_DATA")
        layout.operator("mesh.primitive_imvu_female_body_add", text="Female", icon="MOD_ARMATURE")
        layout.operator("mesh.primitive_imvu_male_body_add", text="Male", icon="OUTLINER_DATA_ARMATURE")
        layout.operator("object.empty_imvu_sit_add", icon="LAYER_USED")
        layout.operator("object.empty_imvu_stand_add", icon="RADIOBUT_OFF")
