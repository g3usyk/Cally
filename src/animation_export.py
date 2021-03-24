from bpy.props import (
    BoolProperty,
    EnumProperty,
    StringProperty,
)
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

    scaling = {'100'}

    def update_scale(self, context):
        """Checks if scale enum has an invalid state.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        if len(self.scale) == 0 or len(self.scale) > 1:
            self.scale = self.scaling
        self.scaling = self.scale

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
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):
        export_xaf(context, self.filepath, float(next(iter(self.scale))),
                   context.scene.render.fps, self.debug)
        return {'FINISHED'}
