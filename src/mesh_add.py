import bpy


class VIEW3D_MT_mesh_imvu_female(bpy.types.Menu):
    """Submenu for IMVU female mesh primitives"""
    bl_idname = "VIEW3D_MT_mesh_imvu_female"
    bl_label = "Female"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_imvu_female_body_add", icon="OUTLINER_OB_ARMATURE")
        layout.operator("mesh.primitive_imvu_female_head_add", icon="MONKEY")
        layout.operator("mesh.primitive_imvu_female_torso_add", icon="USER")
        layout.operator("mesh.primitive_imvu_female_hands_add", icon="VIEW_PAN")
        layout.operator("mesh.primitive_imvu_female_thighs_add", icon="CONSTRAINT_BONE")
        layout.operator("mesh.primitive_imvu_female_legs_add", icon="GROUP_BONE")
        layout.operator("mesh.primitive_imvu_female_feet_add", icon="MOD_DYNAMICPAINT")


class VIEW3D_MT_mesh_imvu_male(bpy.types.Menu):
    """Submenu for IMVU male mesh primitives"""
    bl_idname = "VIEW3D_MT_mesh_imvu_male"
    bl_label = "Male"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_imvu_male_body_add", icon="OUTLINER_OB_ARMATURE")
        layout.operator("mesh.primitive_imvu_male_head_add", icon="MONKEY")
        layout.operator("mesh.primitive_imvu_male_torso_add", icon="USER")
        layout.operator("mesh.primitive_imvu_male_hands_add", icon="VIEW_PAN")
        layout.operator("mesh.primitive_imvu_male_legs_add", icon="GROUP_BONE")
        layout.operator("mesh.primitive_imvu_male_calfs_add", icon="CONSTRAINT_BONE")
        layout.operator("mesh.primitive_imvu_male_feet_add", icon="MOD_DYNAMICPAINT")


class VIEW3D_MT_mesh_imvu(bpy.types.Menu):
    """Menu for IMVU mesh primitives"""
    bl_idname = "VIEW3D_MT_mesh_imvu"
    bl_label = "IMVU"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("VIEW3D_MT_mesh_imvu_female", icon="MOD_ARMATURE")
        layout.menu("VIEW3D_MT_mesh_imvu_male", icon="OUTLINER_DATA_ARMATURE")
