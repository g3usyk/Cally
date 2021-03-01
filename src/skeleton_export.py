import bpy
from bpy.props import (
    StringProperty,
)
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from .xfile.xsf import export_xsf


class CalSkeletonExporter(Operator, ExportHelper):
    """Exports selected empty objects as a Cal3D XSF file.

    """
    bl_idname = "export_scene.export_xsf"
    bl_label = "Export XSF"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ".xsf"

    filter_glob: StringProperty(
        default="*.xsf",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        export_xsf(context)
        return {'FINISHED'}
