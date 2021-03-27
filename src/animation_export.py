import bpy

from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from .xfile.xaf import export_xaf


class CalAnimationExporter(Operator, ExportHelper):
    """Exports selected armature as a Cal3D XAF file"""
    bl_idname = "export_scene.export_xaf"
    bl_label = "Export XAF"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ".xaf"

    filter_glob: StringProperty(
        default="*.xaf",
        options={'HIDDEN'},
        maxlen=255,
    )

    debug: BoolProperty(
        name="Debug",
        description="For debugging output only",
        default=False,
    )

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        options={"ENUM_FLAG"},
        items=(
            ('100', "Auto", "Default upscaled resolution"),
            ('1', "Native", "Client resolution")
        ),
        default='100'
    )

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object.type == 'ARMATURE'

    def execute(self, context: bpy.types.Context):
        export_xaf(context, self.filepath, float(self.scale), context.scene.render.fps, self.debug)
        return {'FINISHED'}
