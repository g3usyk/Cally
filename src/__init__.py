bl_info = {
    "name": "Cal3D Toolkit",
    "author": "hsoju",
    "version": (1, 0, 3),
    "blender": (2, 90, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Cal3D objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}


import bpy
import bmesh
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy_extras.io_utils import ExportHelper
from xml.etree import cElementTree as et

sub_map = {}
sub_prev = ""
active_sub = ""

class XVertex():
    def __init__(self):
        self.posn = []
        self.norm = []
        self.uv = []
        self.color = []
        self.bone = 0

    def parse(self, idx, u_idx, scale):
        xvert = et.Element('vertex')
        xvert.attrib['numinfluences'] = '1'
        xvert.attrib['id'] = str(idx)

        xposn = et.Element('pos')
        xposn.text = ''.join([(str(p * scale) + ' ') for p in self.posn])[:-1]
        xnorm = et.Element('norm')
        xnorm.text = ''.join([(str(n) + ' ') for n in self.norm])[:-1]
        xcol = et.Element('color')
        xcol.text = ''.join([(str(c) + ' ') for c in self.color])[:-1]
        xuv = et.Element('texcoord')
        xuv.text = str(self.uv[u_idx][0]) + ' ' + str(abs(1 - self.uv[u_idx][1]))
        xinf = et.Element('influence')
        xinf.attrib['id'] = self.bone
        xinf.text = '1'

        xvert.append(xposn)
        xvert.append(xnorm)
        xvert.append(xcol)
        xvert.append(xuv)
        xvert.append(xinf)

        return xvert


class XFace():
    def __init__(self):
        self.ix = []

    def parse(self, idxs):
        xfac = et.Element('face')
        xfac.attrib['vertexid'] = ''.join([(str(idxs[i[0]][i[1]]) + ' ') for i in self.ix])[:-1]
        return xfac


def export_xmf(context, filepath, pretty, scale, tri):
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))

    for obj in objs:
        coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
        norms = [v.normal for v in obj.data.vertices]
        xverts = []
        bone_id = sub_map[obj.name][1]
        if bone_id == "":
            bone_id = '0'
        for x in range(0, len(obj.data.vertices)):
            next_vert = XVertex()
            next_vert.posn.append(coords[x][0])
            next_vert.posn.append(coords[x][1])
            next_vert.posn.append(coords[x][2])
            next_vert.norm.append(norms[x][0])
            next_vert.norm.append(norms[x][1])
            next_vert.norm.append(norms[x][2])
            next_vert.color = ['1', '1', '1']
            next_vert.bone = bone_id
            xverts.append(next_vert)

        xfaces = []
        
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        if tri:
            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
        uv_layer = bm.loops.layers.uv.active
        for face in bm.faces:
            next_face = XFace()
            for v, l in zip(face.verts, face.loops):
                v_idx = v.index
                uv_coords = l[uv_layer].uv
                next_uv = [uv_coords[0], uv_coords[1]]
                if next_uv in xverts[v_idx].uv:
                    next_face.ix.append([v_idx, xverts[v_idx].uv.index(next_uv)])
                else:
                    next_face.ix.append([v_idx, len(xverts[v_idx].uv)])
                    xverts[v_idx].uv.append(next_uv)
            xfaces.append(next_face)
        bm.free()

        sub = et.Element('submesh')
        sub.attrib['numfaces'] = str(len(xfaces))
        sub.attrib['numlodsteps'] = '0'
        sub.attrib['numsprings'] = '0'
        sub.attrib['nummorphs'] = '0'
        sub.attrib['numtexcoords'] = '1'
        sub.attrib['material'] = str(sub_map[obj.name][2])

        v_id = 0
        v_ids = []
        for y in range(0, len(xverts)):
            v_ids.append([])
            for z in range(0, len(xverts[y].uv)):
                elemvert = xverts[y].parse(v_id, z, scale)
                sub.append(elemvert)
                v_ids[y].append(v_id)
                v_id += 1

        sub.attrib['numvertices'] = str(v_id)

        for face in xfaces:
            elemface = face.parse(v_ids)
            sub.append(elemface)

        root.append(sub)

    

    xtext = et.tostring(root).decode('utf8')
    if pretty:
        xtext = xtext.upper()
        xtext = xtext.replace('<', '\n<')
        xtext = xtext.replace('\n</', '</')
    f = open(filepath, 'w', encoding='utf-8')
    f.write("<HEADER MAGIC=\"XMF\" VERSION=\"919\"/>")
    f.write("%s" % xtext)
    f.close()


class CalMeshExporter(Operator, ExportHelper):
    """Export selected objects as a Cal3D XMF file"""
    bl_idname = "export_scene.export_xmf"
    bl_label = "Export XMF"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ".xmf"

    filter_glob: StringProperty(
        default="*.xmf",
        options={'HIDDEN'},
        maxlen=255,
    )

    pretty: BoolProperty(
        name="Pretty-Print",
        description="For debugging only",
        default=False,
    )

    def update_subs(self, context):
        self.body = sub_map[self.subs][0]
        self.bone = sub_map[self.subs][1]
        self.mtl = sub_map[self.subs][2]

    def sub_items(self, context):
        global sub_map
        sub_names = [obj.name for obj in context.selected_objects if obj.type == 'MESH']
        items = []
        # Add submeshes to drop-down menu
        for x in range(0, len(sub_names)):
            next_sub = (sub_names[x], sub_names[x], "")
            items.append(next_sub)
            # Add submeshes to bone lookup dictionary
            if sub_names[x] not in sub_map:
                sub_map[sub_names[x]] = ['OPT_A', '0', 0]
        sub_keys = sub_map.keys()
        prev_sub = None
        # Remove submeshes from bone lookup dictionary if deleted
        for sub in sub_keys:
            if sub not in sub_names:
                sub_map.pop(sub, 'None')
                if prev_sub is None:
                    self.body = 'OPT_A'
                    self.bone = '0'
                    self.mtl = 0
                else:
                    self.subs = prev_sub
            else:
                prev_sub = sub
        return items

    subs: EnumProperty(
        name="Submesh",
        description="Selected objects in scene",
        items=sub_items,
        update=update_subs
    )

    def update_body(self, context):
        global sub_map
        sub_map[self.subs][0] = self.body
        self.bone = self.bone

    body: EnumProperty(
        name="Body Part",
        description="Attaches mesh to body part",
        items=(
            ('OPT_A', "Root", "Default"),
            ('OPT_B', "Head", "Used for head"),
            ('OPT_C', "Neck", "Used for neck"),
            ('OPT_D', "Torso", "Used for upper body"),
            ('OPT_E', "Left Arm", "Used for left arm from avatar's perspective"),
            ('OPT_F', "Right Arm", "Used for right arm from avatar's perspective"),
            ('OPT_G', "Left Hand", "Used for left hand from avatar's perspective"),
            ('OPT_H', "Right Hand", "Used for right hand from avatar's perspective"),
            ('OPT_I', "Left Leg", "Used for left leg from avatar's perspective"),
            ('OPT_J', "Right Leg", "Used for right leg from avatar's perspective")
        ),
        default='OPT_A',
        update=update_body
    )

    def update_bone(self, context):
        global sub_map
        sub_map[self.subs][1] = self.bone

    def bone_items(self, context):
        items = []
        if self.body == 'OPT_A':
            items.append(('0', "Master Root", "'Female03MasterRoot'\n   ID: 0"))
            items.append(('1', "Pelvis", "'PelvisNode'\n   ID: 1"))
        elif self.body == 'OPT_B':
            items.append(('22', "Head", "'Head'\n   ID: 22"))
        elif self.body == 'OPT_C':
            items.append(('18', "Collarbone", "'Neck01'\n   ID: 18"))
            items.append(('19', "Lower Throat", "'Neck02'\n   ID: 19"))
            items.append(('20', "Upper Throat", "'Neck03'\n   ID: 20"))
            items.append(('21', "Jaw", "'Neck04'\n   ID: 21"))
        elif self.body == 'OPT_D':
            items.append(('14', "Belly", "'Spine01'\n   ID: 14"))
            items.append(('15', "Abs", "'Spine02'\n   ID: 15"))
            items.append(('16', "Ribs", "'Spine03'\n   ID: 16"))
            items.append(('17', "Chest", "'Spine04'\n   ID: 17"))
        elif self.body == 'OPT_E':
            items.append(('24', "Trap", "'lfClavicle'\n   ID: 24"))
            items.append(('25', "Shoulder", "'lfShoulder'\n   ID: 25"))
            items.append(('26', "Bicep", "'lfBicep'\n   ID: 26"))
            items.append(('27', "Elbow", "'lfElbow'\n   ID: 27"))
        elif self.body == 'OPT_F':
            items.append(('55', "Trap", "'rtClavicle'\n   ID: 55"))
            items.append(('56', "Shoulder", "'rtShoulder'\n   ID: 56"))
            items.append(('57', "Bicep", "'rtBicep'\n   ID: 57"))
            items.append(('58', "Elbow", "'rtElbow'\n   ID: 58"))
        elif self.body == 'OPT_G':
            items.append(('28', "Wrist", "'lfWrist'\n   ID: 28"))
            items.append(('29', "Hand", "'lfHand'\n   ID: 29"))
            items.append(('41', "Pinky Knuckle", "'lfFingerPinky01'\n   ID: 41"))
            items.append(('42', "Pinky Middle", "'lfFingerPinky02'\n   ID: 42"))
            items.append(('43', "Pinky Tip", "'lfFingerPinky03'\n   ID: 43"))
            items.append(('51', "Ring Knuckle", "'lfFingerRing01'\n   ID: 51"))
            items.append(('52', "Ring Middle", "'lfFingerRing02'\n   ID: 52"))
            items.append(('53', "Ring Tip", "'lfFingerRing03'\n   ID: 53"))
            items.append(('31', "Middle Knuckle", "'lfFingerMiddle01'\n   ID: 31"))
            items.append(('32', "Middle Middle", "'lfFingerMiddle02'\n   ID: 32"))
            items.append(('33', "Middle Tip", "'lfFingerMiddle03'\n   ID: 33"))
            items.append(('46', "Index Knuckle", "'lfFingerIndex01'\n   ID: 46"))
            items.append(('47', "Index Middle", "'lfFingerIndex02'\n   ID: 47"))
            items.append(('48', "Index Tip", "'lfFingerIndex03'\n   ID: 48"))
            items.append(('36', "Thumb Knuckle", "'lfThumb01'\n   ID: 36"))
            items.append(('37', "Thumb Middle", "'lfThumb02'\n   ID: 37"))
            items.append(('38', "Thumb Tip", "'lfThumb03'\n   ID: 38"))
        elif self.body == 'OPT_H':
            items.append(('59', "Wrist", "'rtWrist'\n   ID: 59"))
            items.append(('60', "Hand", "'rtHand'\n   ID: 60"))
            items.append(('72', "Pinky Knuckle", "'rtFingerPinky01'\n   ID: 72"))
            items.append(('73', "Pinky Middle", "'rtFingerPinky02'\n   ID: 73"))
            items.append(('74', "Pinky Tip", "'rtFingerPinky03'\n   ID: 74"))
            items.append(('82', "Ring Knuckle", "'rtFingerRing01'\n   ID: 82"))
            items.append(('83', "Ring Middle", "'rtFingerRing02'\n   ID: 83"))
            items.append(('84', "Ring Tip", "'rtFingerRing03'\n   ID: 84"))
            items.append(('62', "Middle Knuckle", "'rtFingerMiddle01'\n   ID: 62"))
            items.append(('63', "Middle Middle", "'rtFingerMiddle02'\n   ID: 63"))
            items.append(('63', "Middle Tip", "'rtFingerMiddle03'\n   ID: 64"))
            items.append(('77', "Index Knuckle", "'rtFingerIndex01'\n   ID: 77"))
            items.append(('78', "Index Middle", "'rtFingerIndex02'\n   ID: 78"))
            items.append(('79', "Index Tip", "'rtFingerIndex03'\n   ID: 79"))
            items.append(('67', "Thumb Knuckle", "'rtThumb01'\n   ID: 67"))
            items.append(('68', "Thumb Middle", "'rtThumb02'\n   ID: 68"))
            items.append(('69', "Thumb Tip", "'rtThumb03'\n   ID: 69"))
        elif self.body == 'OPT_I':
            items.append(('2', "Hip", "'lfHip'\n   ID: 2"))
            items.append(('3', "Thigh", "'lfThigh'\n   ID: 3"))
            items.append(('4', "Calf", "'lfCalf'\n   ID: 4"))
            items.append(('5', "Foot", "'lfFoot'\n   ID: 5"))
            items.append(('6', "Toes", "'lfToes'\n   ID: 6"))
        elif self.body == 'OPT_J':
            items.append(('8', "Hip", "'rtHip'\n   ID: 8"))
            items.append(('9', "Thigh", "'rtThigh'\n   ID: 9"))
            items.append(('10', "Calf", "'rtCalf'\n   ID: 10"))
            items.append(('11', "Foot", "'rtFoot'\n   ID: 11"))
            items.append(('12', "Toes", "'rtToes'\n   ID: 12"))
        return items

    bone: EnumProperty(
        name="Bone",
        description="Specifies imvu's skeleton",
        items=bone_items,
        update=update_bone
    )

    def update_mtl(self, context):
        global sub_map
        sub_map[self.subs][2] = self.mtl

    mtl: IntProperty(
        name="Material ID",
        description="Assigns meshes to material slots (id's separated by whitespace)",
        min=0,
        max=100,
        default=0,
        update=update_mtl
    )

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        options={"ENUM_FLAG"},
        items=(
            ('100', "Auto", "Default upscaled resolution"),
            ('1', "Native", "Client resolution")
        ),
        default={'100'},
    )

    tri: BoolProperty(
        name="Triangulate",
        description="Converts all faces to triangles for imvu compatibility",
        default=True,
    )

    def execute(self, context):
        export_xmf(context, self.filepath,
                    self.pretty, float(next(iter(self.scale))), self.tri)
        return {'FINISHED'}

    def cancel(self, context):
        pass


def menu_export_button(self, context):
    self.layout.operator(CalMeshExporter.bl_idname, text="Cal3D Mesh (.xmf)")


def export_xmf_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.export", "files/import_export.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(CalMeshExporter)
    bpy.utils.register_manual_map(export_xmf_manual_map)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_button)


def unregister():
    bpy.utils.unregister_class(CalMeshExporter)
    bpy.utils.unregister_manual_map(export_xmf_manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_button)


if __name__ == "__main__":
    register()
