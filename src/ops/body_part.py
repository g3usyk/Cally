from ..avi.proxy import Proxy


class BodyPart:
    """Abstracts creation of body part mesh.

    """

    def __init__(self, gender: str, part: str):
        self.gender = gender.lower()
        self.part = part.lower()
        self.bl_idname = f'mesh.primitive_imvu_{self.gender}_{self.part}_add'
        self.bl_label = self.part.capitalize()
        self.bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mesh = Proxy(f'{self.gender[0].upper()}.{self.part.capitalize()}',
                     ["assets", self.gender, f'{self.part}.pickle'])
        mesh.to_mesh()
        return {'FINISHED'}
