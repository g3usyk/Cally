from bpy.types import Panel

class CAL_MESH_PT_export(Panel):
    """Export panel for meshes"""
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'pretty')
        layout.prop(operator, 'weight')
        layout.prop(operator, 'subs')
        if next(iter(operator.weight)) == 'MANUAL':
            layout.prop(operator, 'body')
            layout.prop(operator, 'bone')
        layout.prop(operator, 'mtl')
        layout.prop(operator, 'scale')
