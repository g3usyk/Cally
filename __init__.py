bl_info = {
    "name": "Cal3D Toolkit",
    "author": "hsoju",
    "version": (1, 0, 6),
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
from .src.mesh_add import VIEW3D_MT_mesh_imvu, VIEW3D_MT_mesh_imvu_male
from .src.ops import head, torso, hands, legs, calfs, feet


def mesh_export_button(self, context):
    self.layout.operator(CalMeshExporter.bl_idname, text="Cal3D Mesh (.xmf)")


def mesh_add_menu(self, context):
    self.layout.menu(VIEW3D_MT_mesh_imvu.bl_idname, text="IMVU", icon="INFO")


def default_armature_menu(self, context):
    self.layout.operator(DefaultSkeleton.bl_idname, icon='BONE_DATA')


def manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.export", "files/import_export.html"),
    )
    return url_manual_prefix, url_manual_mapping


classes = (
    CalMeshExporter,
    DefaultSkeleton,
    head.MaleHead,
    torso.MaleTorso,
    hands.MaleHands,
    legs.MaleLegs,
    calfs.MaleCalfs,
    feet.MaleFeet,
    VIEW3D_MT_mesh_imvu_male,
    VIEW3D_MT_mesh_imvu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.append(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.append(default_armature_menu)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.remove(default_armature_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu)


if __name__ == "__main__":
    register()
