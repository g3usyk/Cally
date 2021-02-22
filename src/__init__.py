bl_info = {
    "name": "Cal3D Toolkit",
    "author": "hsoju",
    "version": (1, 0, 5),
    "blender": (2, 90, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Cal3D objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
from src.mesh_export import CalMeshExporter
from src.skeleton import DefaultSkeleton

def mesh_export_button(self, context):
    self.layout.operator(CalMeshExporter.bl_idname, text="Cal3D Mesh (.xmf)")

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
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.append(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.append(default_armature_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_manual_map(manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(mesh_export_button)
    bpy.types.VIEW3D_MT_armature_add.remove(default_armature_menu)


if __name__ == "__main__":
    register()
