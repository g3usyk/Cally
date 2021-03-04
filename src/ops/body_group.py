from ..avi.proxy_group import ProxyGroup


class BodyGroup:
    """Abstracts creation of a group of body meshes.

    """

    def __init__(self, gender: str, parts: list, uvs=True, weights=True):
        self.gender = gender.lower()
        self.parts = [p.lower() for p in parts]
        self.bl_idname = f'mesh.primitive_imvu_{self.gender}_body_add'
        self.bl_label = 'Body'
        self.bl_options = {'REGISTER', 'UNDO'}
        self.uvs = uvs
        self.weights = weights

    def execute(self, selected_parts):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            selected_parts ():

        Returns:
            A set containing the success state of the method.

        """
        proxies = []
        g = self.gender[0].upper()
        for selection, part in zip(selected_parts, self.parts):
            if selection:
                label = f'{g}.{part.capitalize()}'
                file_path = ["assets", self.gender, f'{part}.pickle']
                proxies.append((label, file_path))
        mesh_group = ProxyGroup(proxies)
        mesh_group.to_mesh(f'{g}_Body', self.uvs, self.weights)
        return {'FINISHED'}
