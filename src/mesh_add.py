import bpy


class VIEW3D_MT_mesh_imvu_female(bpy.types.Menu):
    """Outlines submenu layout for imvu female mesh primitives.

    """
    bl_idname = "VIEW3D_MT_mesh_imvu_female"
    bl_label = "Female"

    def draw(self, context):
        """Determines the order of imvu mesh primitives in the female submenu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
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
    """Outlines submenu layout for imvu male mesh primitives.

    """
    bl_idname = "VIEW3D_MT_mesh_imvu_male"
    bl_label = "Male"

    def draw(self, context):
        """Determines the order of imvu mesh primitives in the male submenu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
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
    """Outlines menu layout for imvu mesh primitives.

    """
    bl_idname = "VIEW3D_MT_mesh_imvu"
    bl_label = "IMVU"

    def draw(self, context):
        """Determines the order of imvu submenus in the mesh add menu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("VIEW3D_MT_mesh_imvu_female", icon="MOD_ARMATURE")
        layout.menu("VIEW3D_MT_mesh_imvu_male", icon="OUTLINER_DATA_ARMATURE")
