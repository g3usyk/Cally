import bpy
from bpy.props import (
    StringProperty,
)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from .arm.master_root import add_master_root
from .xfile.xaf import import_xaf


class CalAnimationImporter(Operator, ImportHelper):
    """Load a XAF file"""
    bl_idname = "import_scene.xaf"
    bl_label = "Import XAF"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    filename_ext = ".xaf"

    filter_glob: StringProperty(
        default="*.xaf",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        obj = context.active_object
        if not context.active_object or context.active_object.type != 'ARMATURE':
            obj = add_master_root()
            obj.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')
        import_xaf(obj, self.filepath)
        return {'FINISHED'}
