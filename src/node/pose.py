import bpy


class Pose:

    def __init__(self, pose_type, context):
        self.pose_type = pose_type
        if "Spots" not in bpy.data.collections:
            spots = bpy.data.collections.new("Spots")
            context.scene.collection.children.link(spots)
            layer_col = bpy.context.view_layer.layer_collection.children[spots.name]
            bpy.context.view_layer.active_layer_collection = layer_col
            bpy.ops.object.empty_add(type='SPHERE')
            handle = bpy.context.active_object
            handle.name = "Handle"
            bpy.context.object.empty_display_size = 0.20

    def to_scene(self, primitive: str):
        layer_col = bpy.context.view_layer.layer_collection.children["Spots"]
        bpy.context.view_layer.active_layer_collection = layer_col
        bpy.ops.object.empty_add(type=primitive)
        spot = bpy.context.active_object
        spot.name = f'{self.pose_type}'
