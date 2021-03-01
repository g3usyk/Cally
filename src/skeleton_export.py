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

    pretty: BoolProperty(
        name="Pretty-Print",
        description="For debugging only",
        default=False,
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
        return any([obj.type == 'EMPTY' for obj in context.selected_objects])

    def execute(self, context):
        export_xsf(context, self.filepath, float(next(iter(self.scale))), self.pretty)
        return {'FINISHED'}
