from ..avi.proxy import Proxy


class BodyPart:
    """Abstracts creation of a body part mesh.

    """

    def __init__(self, gender: str, part: str, uvs=True):
        self.gender = gender.lower()
        self.part = part.lower()
        self.bl_idname = f'mesh.primitive_imvu_{self.gender}_{self.part}_add'
        self.bl_label = self.part.capitalize()
        self.bl_options = {'REGISTER', 'UNDO'}
        self.uvs = uvs

    def execute(self, context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:
            A set containing the success state of the method.

        """
        mesh = Proxy(f'{self.gender[0].upper()}.{self.part.capitalize()}',
                     ["assets", self.gender, f'{self.part}.pickle'])
        mesh.to_mesh(uvs=self.uvs)
        return {'FINISHED'}
