import bpy

from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from .xfile.xsf import export_xsf


class CalSkeletonExporter(Operator, ExportHelper):
    """Exports selected empty objects as a Cal3D XSF file"""
    bl_idname = "export_scene.export_xsf"
    bl_label = "Export XSF"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ".xsf"

    filter_glob: StringProperty(
        default="*.xsf",
        options={'HIDDEN'},
        maxlen=255,
    )

    def category_items(self, context: bpy.types.Context) -> list:
        items = []
        items.extend((
            ('FURNITURE', "Furniture", "Used with furniture meshes"),
            ('ROOM', "Room", "Used with room meshes"),
        ))
        return items

    category: EnumProperty(
        name="Type",
        items=category_items,
    )

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        items=(
            ('100', "Auto", "Default upscaled resolution"),
            ('1', "Native", "Client resolution")
        ),
        default='100',
    )

    @classmethod
    def poll(cls, context: bpy.types.Context):
        for obj in context.selected_objects:
            if obj.type == 'EMPTY':
                if obj.empty_display_type != 'SPHERE':
                    return True
        return False

    def execute(self, context: bpy.types.Context):
        export_xsf(context, self.filepath, self.category, float(self.scale))
        return {'FINISHED'}
