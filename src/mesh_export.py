import re
from typing import List, Set, Tuple

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import Context, Operator
from bpy_extras.io_utils import ExportHelper

from .maps.ids import IDMap
from .maps.names import NameMap
from .xfile.xmf import export_xmf


def get_bone(obj_name: str) -> str:
    obj = bpy.data.objects[obj_name]
    group = obj.vertex_groups.active if obj.vertex_groups else None
    bone = 'Female03MasterRoot'
    if group:
        bone = group.name if group.name in IDMap.mapping else NameMap.lookup(0)
    return bone


def get_material(obj_name: str) -> int:
    obj = bpy.data.objects[obj_name]
    mtl = obj.active_material.name if obj.active_material else None
    material = 0
    if mtl:
        mtl_id = re.sub(r'\D', '', mtl)
        if mtl_id != '':
            material = int(mtl_id)
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

    def update_subs(self, context: Context):
        """Configures child menus to reflect changes in submesh menu.

        Args:
            context (): A bpy context containing data in the current 3d view.
        """
        self.bone = get_bone(self.subs)
        self.mtl = get_material(self.subs)

    def sub_items(self, context: Context) -> List[Tuple[str, ...]]:
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
    def poll(cls, context: Context) -> bool:
        return any(((obj.type == 'MESH') for obj in context.selected_objects))

    def execute(self, context: Context) -> Set[str]:
        """Calls xmf file generation method.

        Args:
            context (bpy.types.Context): A bpy context containing data in the current 3d view.

        Returns:
            set: The success state of the execution.
        """
        submap = {obj.name: {'bone': IDMap.lookup(get_bone(obj.name)), 'material': get_material(obj.name)}
                  for obj in context.selected_objects if obj.type == 'MESH'}
        current_mode = context.object.mode
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        export_xmf(context, self.filepath, submap, float(self.scale), self.weight, self.auto)
        bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    def draw(self, context: Context):
        """Determines the format for showing options in the file export dialog menu.

        Args:
            context (bpy.types.Context): A bpy context containing data in the current 3d view.
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
