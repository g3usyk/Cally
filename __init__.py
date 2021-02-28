bl_info = {
    "name": "Cally",
    "author": "hsoju",
    "version": (1, 0, 9),
    "blender": (2, 90, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Cal3D objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
from .src.mesh_export import CalMeshExporter
from .src.skeleton import DefaultSkeleton
from .src.mesh_add import (
    VIEW3D_MT_mesh_imvu,
    VIEW3D_MT_mesh_imvu_female,
    VIEW3D_MT_mesh_imvu_male,
)
from .src.ops.female import f_body, f_head, f_torso, f_hands, f_legs, f_thighs, f_feet
from .src.ops.male import m_body, m_head, m_torso, m_hands, m_legs, m_calfs, m_feet


def mesh_export_button(self, context):
    """Targets exporter class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (): A bpy context containing data in the current 3d view.
    """
    self.layout.operator(CalMeshExporter.bl_idname, text="Cal3D Mesh (.xmf)")


def mesh_add_menu(self, context):
    """Targets mesh menu class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (): A bpy context containing data in the current 3D view.
    """
    self.layout.menu(VIEW3D_MT_mesh_imvu.bl_idname, icon="INFO")


def default_armature_menu(self, context):
    """Targets armature menu class on menu button press.

    Args:
        self (): A reference to this bpy dynamic draw function.
        context (): A bpy context containing data in the current 3d view.
    """
    self.layout.operator(DefaultSkeleton.bl_idname, icon='BONE_DATA')


def manual_map():
    """Defines documentation for addon.

    Returns: A tuple containing a hyperlink to the relevant documentation.

    """
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.export", "files/import_export.html"),
    )
    return url_manual_prefix, url_manual_mapping


classes = (
    CalMeshExporter,
    DefaultSkeleton,
    f_body.FemaleBody,
    f_head.FemaleHead,
    f_torso.FemaleTorso,
    f_hands.FemaleHands,
    f_legs.FemaleLegs,
    f_thighs.FemaleThighs,
    f_feet.FemaleFeet,
    m_body.MaleBody,
    m_head.MaleHead,
    m_torso.MaleTorso,
    m_hands.MaleHands,
    m_legs.MaleLegs,
    m_calfs.MaleCalfs,
    m_feet.MaleFeet,
    VIEW3D_MT_mesh_imvu_female,
    VIEW3D_MT_mesh_imvu_male,
    VIEW3D_MT_mesh_imvu,
)


def register():
    """Defines behaviour when addon installs onto Blender.

    """
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.append(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.append(default_armature_menu)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu)


def unregister():
    """Defines behaviour when addon uninstalls from Blender.

    """
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.remove(default_armature_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu)


if __name__ == "__main__":
    register()
