bl_info = {
    "name": "Cally",
    "author": "hsoju",
    "version": (4, 0, 1),
    "blender": (2, 90, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Cal3D objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy

from .src.animation_export import CalAnimationExporter
from .src.animation_import import CalAnimationImporter
from .src.mesh_export import CalMeshExporter
from .src.mesh_import import CalMeshImporter
from .src.morph_export import CalMorphExporter
from .src.skeleton_export import CalSkeletonExporter
from .src.ops.skeleton import DefaultSkeleton
from .src.ops import sit, stand
from .src.ops import f_body, m_body
from .src.imvu_add import VIEW3D_MT_imvu


def animation_export_button(self, context: bpy.types.Context):
    """Targets animation exporter class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalAnimationExporter.bl_idname, text="Cal3D Animation (.xaf)")


def animation_import_button(self, context: bpy.types.Context):
    """Targets animation importer class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalAnimationImporter.bl_idname, text="Cal3D Animation (.xaf)")


def mesh_export_button(self, context: bpy.types.Context):
    """Targets mesh exporter class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalMeshExporter.bl_idname, text="Cal3D Mesh (.xmf)")


def mesh_import_button(self, context: bpy.types.Context):
    """Targets mesh importer class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalMeshImporter.bl_idname, text="Cal3D Mesh (.xmf)")


def morph_export_button(self, context: bpy.types.Context):
    """Targets morph exporter class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalMorphExporter.bl_idname, text="Cal3D Morph (.xpf)")


def skeleton_export_button(self, context: bpy.types.Context):
    """Targets skeleton exporter class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.operator(CalSkeletonExporter.bl_idname, text="Cal3D Skeleton (.xsf)")


def imvu_add_menu(self, context: bpy.types.Context):
    """Targets object add menu for imvu primitives.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (bpy.types.Context): The context containing data for the current 3d view.
    """
    self.layout.menu(VIEW3D_MT_imvu.bl_idname, icon="INFO")


def manual_map() -> tuple:
    """Defines documentation for addon.

    Returns:
        tuple: A hyperlink to the relevant documentation.

    """
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.export", "files/import_export.html"),
    )
    return url_manual_prefix, url_manual_mapping


classes = (
    CalAnimationExporter,
    CalAnimationImporter,
    CalMeshExporter,
    CalMeshImporter,
    CalMorphExporter,
    CalSkeletonExporter,
    DefaultSkeleton,
    sit.SittingSpot,
    stand.StandingSpot,
    f_body.FemaleBody,
    m_body.MaleBody,
    VIEW3D_MT_imvu,
)


def register():
    """Defines behaviour when addon installs onto Blender.

    """
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.append(animation_export_button)
    bpy.types.TOPBAR_MT_file_import.append(animation_import_button)
    bpy.types.TOPBAR_MT_file_export.append(mesh_export_button)
    bpy.types.TOPBAR_MT_file_import.append(mesh_import_button)
    bpy.types.TOPBAR_MT_file_export.append(morph_export_button)
    bpy.types.TOPBAR_MT_file_export.append(skeleton_export_button)
    bpy.types.VIEW3D_MT_add.append(imvu_add_menu)


def unregister():
    """Defines behaviour when addon uninstalls from Blender.

    """
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(animation_export_button)
    bpy.types.TOPBAR_MT_file_import.remove(animation_import_button)
    bpy.types.TOPBAR_MT_file_export.remove(mesh_export_button)
    bpy.types.TOPBAR_MT_file_import.remove(mesh_import_button)
    bpy.types.TOPBAR_MT_file_export.remove(morph_export_button)
    bpy.types.TOPBAR_MT_file_export.remove(skeleton_export_button)
    bpy.types.VIEW3D_MT_add.remove(imvu_add_menu)


if __name__ == "__main__":
    register()
