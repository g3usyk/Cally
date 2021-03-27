import bpy
from bpy.props import (StringProperty, BoolProperty, EnumProperty,
                       IntProperty, FloatProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from .maps.ids import IDMap
from .maps.names import NameMap
from .xfile.xmf import export_xmf


def get_bone(obj) -> str:
    group = bpy.data.objects[obj].vertex_groups.active
    bone = group.name if group and group.name in IDMap.mapping else NameMap.lookup(0)
    return bone


def get_material(obj) -> int:
    mtl = bpy.data.objects[obj].active_material
    material = bpy.data.materials.find(mtl.name) if mtl else 0
    return material


class CalMeshExporter(Operator, ExportHelper):
    """Export selection to a Cal3D XMF file"""
    bl_idname = "export_scene.xmf"
    bl_label = "Export XMF"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ".xmf"

    filter_glob: StringProperty(
        default="*.xmf",
        options={'HIDDEN'},
        maxlen=255,
    )

    auto: BoolProperty(
        name="Auto",
        description="For experienced users only",
        default=True,
    )

    weight: EnumProperty(
        name="Weight",
        description="Specifies body part assignment to mesh",
        items=(
            ('OBJECT', 'Object', 'Used for meshes attached to 1 bone (accessories, furniture, etc.)'),
            ('VERTEX', 'Vertex', 'Used for meshes attached to multiple bones (clothing, etc.)'),
        ),
        default='OBJECT',
    )

    def update_subs(self, context):
        """Configures child menus to reflect changes in submesh menu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        self.bone = get_bone(self.subs)
        self.mtl = get_material(self.subs)

    def sub_items(self, context):
        objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if self.bone == '':
            self.bone = get_bone(objs[0].name)
        if self.mtl == -1:
            self.mtl = get_material(objs[0].name)
        return [(ob.name, ob.name, '') for ob in objs]

    subs: EnumProperty(
        name="Submesh",
        description="Selected objects in scene",
        items=sub_items,
        update=update_subs
    )

    bone: StringProperty(
        name="Bone",
        description="Specifies the bone that the submesh will attach to",
        default="",
    )

    mtl: IntProperty(
        name="Material ID",
        description="Specifies the material id for the submesh",
        soft_min=0,
        max=100,
        default=-1
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
    def poll(cls, context):
        return any([(obj.type == 'MESH') for obj in context.selected_objects])

    def execute(self, context) -> set:
        """Calls xmf file generation method.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:
            set: The success state of the execution.
        """
        submap = {obj.name: {'bone': IDMap.lookup(get_bone(obj.name)), 'material': get_material(obj.name)}
                  for obj in context.selected_objects if obj.type == 'MESH'}
        export_xmf(context, self.filepath, submap, float(self.scale), self.weight, self.auto)
        return {'FINISHED'}

    def draw(self, context):
        """Determines the format for showing options in the file export dialog menu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, 'auto')
        layout.prop(self, 'subs')
        if not self.auto:
            layout.prop(self, 'weight')
            bone_row = layout.row()
            if self.weight == 'OBJECT':
                bone_row.prop(self, 'bone')
            bone_row.enabled = False
            material_row = layout.row()
            material_row.prop(self, 'mtl')
            material_row.enabled = False
            layout.prop(self, 'scale')
