from ..avi.proxy_group import ProxyGroup


class BodyGroup:
    """Abstracts creation of group of body meshes.

    """

    def __init__(self, gender: str, parts: list):
        self.gender = gender.lower()
        self.parts = [p.lower() for p in parts]
        self.bl_idname = f'mesh.primitive_imvu_{self.gender}_body_add'
        self.bl_label = 'Body'
        self.bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        proxies = []
        g = self.gender[0].upper()
        for part in self.parts:
            label = f'{g}.{part.capitalize()}'
            file_path = ["assets", self.gender, f'{part}.pickle']
            proxies.append((label, file_path))
        mesh_group = ProxyGroup(proxies)
        mesh_group.to_mesh(f'{g}_Body')
        return {'FINISHED'}
