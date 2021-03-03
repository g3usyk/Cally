import bpy
from bpy.props import (
    BoolProperty,
    StringProperty,
)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from .xfile.xmf import import_xmf


class CalMeshImporter(Operator, ImportHelper):
    """Load a XMF file"""
    bl_idname = "import_scene.xmf"
    bl_label = "Import XMF"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    filename_ext = ".xmf"

    filter_glob: StringProperty(
        default="*.xmf",
        options={'HIDDEN'},
        maxlen=255,
    )

    uvs: BoolProperty(
        name="Add UVs",
        description="Include uv coordinates in mesh",
        default=True,
    )

    def execute(self, context):
        submeshes = import_xmf(self.filepath)
        for b in submeshes:
            b.to_mesh(smooth=False, uvs=self.uvs)
        return {'FINISHED'}
