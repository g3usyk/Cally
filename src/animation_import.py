import bpy
from bpy.props import EnumProperty, StringProperty
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

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        items=(
            ('100', "Auto", "Default upscaled resolution"),
            ('1', "Native", "Client resolution")
        ),
        default='100',
    )

    def execute(self, context):
        obj = context.active_object
        if context.active_object and context.active_object.type == 'ARMATURE':
            bpy.ops.object.delete()
        obj = add_master_root()
        obj.select_set(True)
        obj.animation_data_clear()
        bpy.ops.object.mode_set(mode='POSE')
        import_xaf(context, obj, self.filepath, float(self.scale),
                   context.scene.render.fps)
        return {'FINISHED'}
