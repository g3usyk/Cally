import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, Operator
from bpy_extras.io_utils import ImportHelper
from itertools import compress
from typing import Set
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

    selection: BoolProperty(
        name="Selected bones",
        description="Export selected pose bones only",
        default=False
    )

    head: BoolProperty(
        name="Head",
        description="Include pose bones for head and neck",
        default=False
    )

    spine: BoolProperty(
        name="Spine",
        description="Include pose bones for spine",
        default=False
    )

    r_arm: BoolProperty(
        name="R Arm",
        description="Include pose bones for right arm",
        default=False
    )

    l_arm: BoolProperty(
        name="L Arm",
        description="Include pose bones for left arm",
        default=False
    )

    r_hand: BoolProperty(
        name="R Hand",
        description="Include pose bones for right hand",
        default=False
    )

    l_hand: BoolProperty(
        name="L Hand",
        description="Include pose bones for left hand",
        default=False
    )

    pelvis: BoolProperty(
        name="Pelvis",
        description="Include pelvis pose bone",
        default=False
    )

    r_leg: BoolProperty(
        name="R Leg",
        description="Include pose bones for right leg",
        default=False
    )

    l_leg: BoolProperty(
        name="L Leg",
        description="Include pose bones for left leg",
        default=False
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

    def execute(self, context: Context) -> Set[str]:
        if check_format(self.filepath) != 'ASCII':
            self.report({'ERROR'}, 'Binary file unsupported. Check .xaf file contents.')
            return {'CANCELLED'}
        if context.active_object and context.active_object.type == 'ARMATURE':
            armature = context.active_object
        else:
            armature = add_master_root()
        bpy.ops.object.mode_set(mode='POSE')
        selected_bones = None
        if self.selection:
            selected_bones = compress(
                ['head', 'spine', 'r_arm', 'l_arm', 'r_hand', 'l_hand', 'pelvis', 'r_leg', 'l_leg'],
                [self.head, self.spine, self.r_arm, self.l_arm, self.r_hand, self.l_hand,
                 self.pelvis, self.r_leg, self.l_leg])
        import_xaf(context, armature, self.filepath, float(self.scale), self.selection, selected_bones,
                   context.scene.render.fps)
        body_parts = []
        if self.link and len(armature.children) == 0:
            bpy.ops.object.mode_set(mode='OBJECT')
            body_parts.extend(BodyGroup.default_parts(self.gender))
            link_bones(body_parts, armature)
            context.view_layer.objects.active = armature
            armature.select_set(True)
            bpy.ops.object.mode_set(mode='POSE')
        lock_bones(armature) if self.lock else None
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
        selection_sublayout = layout.column(heading="Limit to")
        selection_sublayout.prop(self, 'selection')
        if self.selection:
            include_sublayout = layout.column(heading="Include")
            include_sublayout.prop(self, 'head')
            include_sublayout.prop(self, 'spine')
            include_sublayout.prop(self, 'r_arm')
            include_sublayout.prop(self, 'l_arm')
            include_sublayout.prop(self, 'r_hand')
            include_sublayout.prop(self, 'l_hand')
            include_sublayout.prop(self, 'pelvis')
            include_sublayout.prop(self, 'r_leg')
            include_sublayout.prop(self, 'l_leg')
        layout.prop(self, 'scale')
