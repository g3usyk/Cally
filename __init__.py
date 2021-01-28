bl_info = {
    "name": "Cal3D Mesh (XMF) format",
    "author": "hsoju",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Cal3D Mesh objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}


import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatVectorProperty
from bpy_extras.io_utils import ExportHelper
from xml.etree import cElementTree as et


class XVertex():
    def __init__(self):
        self.posn = []
        self.norm = []
        self.uv = []
        self.color = []
        self.bone = 0

    def parse(self, idx):
        xvert = et.Element('vertex')
        xvert.attrib['numinfluences'] = '1'
        xvert.attrib['id'] = str(idx)

        xposn = et.Element('pos')
        xposn.text = ''.join([(str(p * 100) + ' ') for p in self.posn])[:-1]
        xnorm = et.Element('norm')
        xnorm.text = ''.join([(str(n) + ' ') for n in self.norm])[:-1]
        xcol = et.Element('color')
        xcol.text = ''.join([(str(c) + ' ') for c in self.color])[:-1]
        xuv = et.Element('texcoord')
        xuv.text = str(self.uv[0]) + ' ' + str(abs(1 - self.uv[1]))
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

    def parse(self):
        xfac = et.Element('face')
        xfac.attrib['vertexid'] = ''.join([(str(i) + ' ') for i in self.ix])[:-1]
        return xfac


def export_xmf(context, filepath, pretty, mtl, bone):
    objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

    root = et.Element('mesh')
    root.attrib['numsubmesh'] = str(len(objs))
    mtl = ''.join(m for m in mtl if m.isdigit() or m.isspace())
    mtls = [m for m in mtl.split()]

    for obj in objs:
        coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
        norms = [v.normal for v in obj.data.vertices]
        xverts = []
        for x in range(0, len(obj.data.vertices)):
            next_vert = XVertex()
            next_vert.posn.append(coords[x][0])
            next_vert.posn.append(coords[x][1])
            next_vert.posn.append(coords[x][2])
            next_vert.norm.append(norms[x][0])
            next_vert.norm.append(norms[x][1])
            next_vert.norm.append(norms[x][2])
            next_vert.color = ['1', '1', '1']
            next_vert.bone = bone
            xverts.append(next_vert)

        xfaces = []
        seen = []

        for face in obj.data.polygons:
            next_face = XFace()
            for v_idx, l_idx in zip(face.vertices, face.loop_indices):
                next_face.ix.append(v_idx)
                if v_idx not in seen:
                    seen.append(v_idx)
                    uv_coords = obj.data.uv_layers.active.data[l_idx].uv
                    xverts[v_idx].uv.append(uv_coords[0])
                    xverts[v_idx].uv.append(uv_coords[1])
            xfaces.append(next_face)

        sub = et.Element('submesh')
        sub.attrib['numvertices'] = str(len(xverts))
        sub.attrib['numfaces'] = str(len(xfaces))
        sub.attrib['numlodsteps'] = '0'
        sub.attrib['numsprings'] = '0'
        sub.attrib['nummorphs'] = '0'
        sub.attrib['numtexcoords'] = '1'
        if len(mtls) == 0:
            sub.attrib['material'] = '0'
        else:
            sub.attrib['material'] = mtls.pop(0)

        for y in range(0, len(xverts)):
            elemvert = xverts[y].parse(y)
            sub.append(elemvert)

        for face in xfaces:
            elemface = face.parse()
            sub.append(elemface)

        root.append(sub)

    xtext = et.tostring(root).decode('utf8')
    if pretty:
        xtext = xtext.replace('<', '\n<')
        xtext = xtext.replace('\n</', '</')
    f = open(filepath, 'w', encoding='utf-8')
    f.write("<header magic=\"xmf\" version=\"919\"/>")
    f.write("%s" % xtext)
    f.close()


class CAL_MESH_exporter(Operator, ExportHelper):
    """Export selected objects as a Cal3D XMF file"""
    bl_idname = "export_scene.export_xmf"
    bl_label = "Export XMF"
    bl_options = {'REGISTER', 'PRESET'}

    # ExportHelper mixin class uses this
    filename_ext = ".xmf"

    filter_glob: StringProperty(
        default="*.xmf",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    pretty: BoolProperty(
        name="Pretty-Print",
        description="For debugging only",
        default=False,
    )

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
    )

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
        items=bone_items
    )

    mtl: StringProperty(
        name="Material ID(s)",
        description="Assigns meshes to material slots (id's separated by whitespace)",
        default='0',
        maxlen=255
    )

    scale: EnumProperty(
        name="Scale",
        description="Applies imvu's scaling factor",
        items=(
            ('100', "1", "Default"),
            ('1', "0.01", "Used for oversized meshes")
        ),
        default='100',
    )

    def execute(self, context):
        export_xmf(context, self.filepath,
                   self.pretty, self.mtl, self.bone)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_export_button(self, context):
    self.layout.operator(CAL_MESH_exporter.bl_idname, text="Cal3D Mesh (.xmf)")


# This allows you to right click on a button and link to documentation
def export_xmf_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.export", "files/import_export.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(CAL_MESH_exporter)
    bpy.utils.register_manual_map(export_xmf_manual_map)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_button)


def unregister():
    bpy.utils.unregister_class(CAL_MESH_exporter)
    bpy.utils.unregister_manual_map(export_xmf_manual_map)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_button)


if __name__ == "__main__":
    register()
