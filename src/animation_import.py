import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, Operator
from bpy_extras.io_utils import ImportHelper
from .arm.master_root import add_master_root, link_bones, lock_bones
from .ops.body_group import BodyGroup
from .xfile.utils import check_format
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

    lock: BoolProperty(
        name="Lock",
        description="Use default transformation locks on each bone",
        default=True,
    )

    link: BoolProperty(
        name="Link",
        description="",
        default=False,
    )

    gender: EnumProperty(
        name="Gender",
        description="Gender type for randomizer",
        items=(
            ('MALE', 'Male', 'Male skeleton'),
            ('FEMALE', 'Female', 'Female Skeleton')
        ),
        default='MALE'
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

    def execute(self, context: Context) -> set:
        if check_format(self.filepath) != 'ASCII':
            self.report({'ERROR'}, 'Binary file unsupported. Check .xaf file contents.')
            return {'CANCELLED'}
        body_parts = []
        if context.active_object and context.active_object.type == 'ARMATURE':
            obj = context.active_object
            if self.link:
                if len(obj.children) == 0:
                    body_parts.extend(BodyGroup.default_parts(self.gender))
        else:
            if self.link:
                body_parts.extend(BodyGroup.default_parts(self.gender))
            obj = add_master_root()
        obj.animation_data_clear()
        bpy.ops.object.mode_set(mode='POSE')
        import_xaf(context, obj, self.filepath, float(self.scale), context.scene.render.fps)
        if self.link:
            link_bones(body_parts, obj)
        if self.lock:
            lock_bones(obj)
        return {'FINISHED'}

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        row.prop(self, 'lock')
        row.prop(self, 'link')
        if self.link:
            layout.prop(self, 'gender')
        layout.prop(self, 'scale')
