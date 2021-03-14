import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    StringProperty,
)
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from .xfile.xsf import export_xsf

scaling = {'100'}
cat = {'FURNITURE'}


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

    def update_category(self, context):
        global cat
        if len(self.category) == 0 or len(self.category) > 1:
            self.category = cat
        cat = self.category

    category: EnumProperty(
        name="Type",
        options={'ENUM_FLAG'},
        items=(
            ('ROOM', "Room", "Used with room meshes"),
            ('FURNITURE', "Furniture", "Used with furniture meshes"),
        ),
        default=cat,
        update=update_category
    )

    def update_scale(self, context):
        """Checks if scale enum has an invalid state.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        global scaling
        if len(self.scale) == 0 or len(self.scale) > 1:
            self.scale = scaling
        scaling = self.scale

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        options={"ENUM_FLAG"},
        items=(
            ('100', "Auto", "Default upscaled resolution"),
            ('1', "Native", "Client resolution")
        ),
        default=scaling,
        update=update_scale
    )

    @classmethod
    def poll(cls, context):
        for obj in context.selected_objects:
            if obj.type == 'EMPTY':
                if obj.empty_display_type != 'SPHERE':
                    return True
        return False

    def execute(self, context):
        export_xsf(context, self.filepath, next(iter(self.category)), float(next(iter(self.scale))))
        return {'FINISHED'}
