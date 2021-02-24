import bpy


class VIEW3D_MT_mesh_imvu_male(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_imvu_male"
    bl_label = "Male"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_imvu_male_head_add", icon="MONKEY")
        layout.operator("mesh.primitive_imvu_male_torso_add", icon="USER")
        layout.operator("mesh.primitive_imvu_male_hands_add", icon="VIEW_PAN")
        layout.operator("mesh.primitive_imvu_male_legs_add", icon="GROUP_BONE")
        layout.operator("mesh.primitive_imvu_male_calfs_add", icon="CONSTRAINT_BONE")
        layout.operator("mesh.primitive_imvu_male_feet_add", icon="MOD_DYNAMICPAINT")


class VIEW3D_MT_mesh_imvu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_imvu"
    bl_label = "IMVU"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("VIEW3D_MT_mesh_imvu_male", text="Male", icon="OUTLINER_DATA_ARMATURE")
