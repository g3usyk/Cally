from bpy.props import BoolProperty, StringProperty
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

    material: BoolProperty(
        name="Include Material ID",
        description="Include linked material ID in mesh",
        default=True,
    )

    norms: BoolProperty(
        name="Include Normals",
        description="Include custom vertex normals in mesh",
        default=True,
    )

    uvs: BoolProperty(
        name="Include UVs",
        description="Include uv coordinates in mesh",
        default=True,
    )

    weights: BoolProperty(
        name="Include Weights",
        description="Include bone weights for mesh",
        default=True,
    )

    morphs: BoolProperty(
        name="Include Morphs",
        description="Include morphs for mesh",
        default=True,
    )

    smooth: BoolProperty(
        name="Smooth Shading",
        description="Apply smooth shading to mesh",
        default=False,
    )

    def execute(self, context) -> set:
        submeshes = import_xmf(self.filepath)
        for base_mesh in submeshes:
            base_mesh.to_mesh(smooth=self.smooth, material=self.material, uvs=self.uvs, norms=self.norms,
                              groups=self.weights, morphs=self.morphs)
        return {'FINISHED'}
