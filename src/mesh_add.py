import bpy


class VIEW3D_MT_mesh_imvu_male(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_imvu_male"
    bl_label = "Male"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_imvu_male_head_add", text="Head")


class VIEW3D_MT_mesh_imvu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_imvu"
    bl_label = "IMVU"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("VIEW3D_MT_mesh_imvu_male", text="Male")
