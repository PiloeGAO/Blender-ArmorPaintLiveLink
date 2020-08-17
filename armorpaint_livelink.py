# -*- coding: utf8 -*-
# python
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "ArmorPaint Live-Link",
    "author": "PiloeGAO (Leo DEPOIX), Spirou4D",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar",
    "description": "Integration of ArmorPaint into Blender Workflow",
    "warning": "Development",
    "wiki_url": "https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink",
    "tracker_url": "https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink/issues",
    "category": "Paint"}

import bpy, os, subprocess, platform
from bpy.types import (Operator,
                        Panel,
                        AddonPreferences, 
                        WindowManager, 
                        PropertyGroup)
from bpy.props import *
from bpy.utils import register_class, unregister_class
from os.path import dirname

SYSTEM = platform.system()
SEP = os.sep

# ------------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------------

def searchTextures(path, textures):
    dir = os.listdir(path)
    for f in dir:
        if(os.path.isfile(path + SEP + f)
            and f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.hdr', '.exr'))):
            if(f.find("_base") > 1): textures[0] = path + SEP + f
            if(f.find("_subs") > 1): textures[1] = path + SEP + f
            if(f.find("_metal") > 1): textures[2] = path + SEP + f
            if(f.find("_rough") > 1): textures[3] = path + SEP + f
            if(f.find("_emission") > 1): textures[4] = path + SEP + f
            if(f.find("_opac") > 1): textures[5] = path + SEP + f
            if(f.find("_nor") > 1): textures[6] = path + SEP + f
    return textures

def reloadTextures():
    # Clean up unused images
    for img in bpy.data.images:
        if not img.users:
            bpy.data.images.remove(img)

    #Reload all File images
    for img in bpy.data.images :
        if img.source == 'FILE' :
            img.reload()

def generateMaterial(path):
    textures = [None,
    None,
    None,
    None,
    None,
    None,
    None]
    
    """
    textures: list structure: - basecolor
    - subsurf
    - metal
    - rough
    - emission
    - opac
    - normalmap
    """
    
    textures = searchTextures(path, textures)
    
    if ('ArmorPaintMtl' in bpy.data.materials):
        reloadTextures()
    else:        
        # Create a new material
        material = bpy.data.materials.new(name="ArmorPaintMtl")
        material.use_nodes = True

        material_output = material.node_tree.nodes.get('Material Output')
        principled_node = material.node_tree.nodes.get('Principled BSDF')

        diff_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for diffuse texture
        diff_texture.name = "diffuse_texture"
        diff_texture.location = -460, 820.0
        if (textures[0] != None): diff_texture.image = bpy.data.images.load(filepath = textures[0])
        
        subs_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for subsurface texture
        subs_texture.name = "subsurface_texture"
        subs_texture.location = -460, 540.0
        if (textures[1] != None): subs_texture.image = bpy.data.images.load(filepath = textures[1])
        
        metallic_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for metallic texture
        metallic_texture.name = "metallic_texture"
        metallic_texture.location = -460, 260.0
        if (textures[2] != None): metallic_texture.image = bpy.data.images.load(filepath = textures[2])
        
        roughness_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for roughness texture
        roughness_texture.name = "roughness_texture"
        roughness_texture.location = -460, -20.0
        if (textures[3] != None): roughness_texture.image = bpy.data.images.load(filepath = textures[3])
        
        emission_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for emission texture
        emission_texture.name = "emission_texture"
        emission_texture.location = -460, -300.0
        if (textures[4] != None): emission_texture.image = bpy.data.images.load(filepath = textures[4])
        
        opacity_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for opacity texture
        opacity_texture.name = "opacity_texture"
        opacity_texture.location = -460, -580.0
        if (textures[5] != None): opacity_texture.image = bpy.data.images.load(filepath = textures[5])
        
        normal_texture = material.node_tree.nodes.new('ShaderNodeTexImage')    #Add node for normal texture
        normal_texture.name = "normal_texture"
        normal_texture.location = -460, -860.0
        if (textures[6] != None): normal_texture.image = bpy.data.images.load(filepath = textures[6])
        

        normal_node = material.node_tree.nodes.new('ShaderNodeNormalMap')    #Add node for normals
        normal_node.location = -200.0, -860.0
        
        
        text_mapping_node = material.node_tree.nodes.new('ShaderNodeMapping')    #Add node for texture mapping
        text_mapping_node.location = -640.0, 200.0
        text_coord_node = material.node_tree.nodes.new('ShaderNodeTexCoord')    #Add node for texture coord
        text_coord_node.location = -800.0, 200.0

        linkNodes = material.node_tree.links

        # link diffuse shader to material
        linkNodes.new(material_output.inputs["Surface"], principled_node.outputs["BSDF"])

        #Link textures to principled
        if (textures[0] != None):
            linkNodes.new(principled_node.inputs["Base Color"], diff_texture.outputs["Color"])
        if (textures[1] != None):
            linkNodes.new(principled_node.inputs["Subsurface Color"], subs_texture.outputs["Color"])
        if (textures[2] != None):
            linkNodes.new(principled_node.inputs["Metallic"], metallic_texture.outputs["Color"])
        if (textures[3] != None):
            linkNodes.new(principled_node.inputs["Roughness"], roughness_texture.outputs["Color"])
        if (textures[4] != None):
            linkNodes.new(principled_node.inputs["Emission"], emission_texture.outputs["Color"])
        if (textures[5] != None):
            linkNodes.new(principled_node.inputs["Alpha"], opacity_texture.outputs["Color"])
        #Normal case
        linkNodes.new(normal_node.inputs["Color"], normal_texture.outputs["Color"])
        linkNodes.new(principled_node.inputs["Normal"], normal_node.outputs["Normal"])

        #Link texture mapping to textures
        linkNodes.new(diff_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(subs_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(metallic_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(roughness_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(emission_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(opacity_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])
        linkNodes.new(normal_texture.inputs["Vector"], text_mapping_node.outputs["Vector"])

        #Link texture coord to texture mapping
        linkNodes.new(text_mapping_node.inputs["Vector"], text_coord_node.outputs["UV"])


        # set activer material to your new material
        bpy.context.object.active_material = material

# ------------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------------

def update_filename(self, context):
    if not self["filename"].endswith(".arm") and self["filename"] != "":
        self["filename"] += ".arm"
    
    objM = bpy.data.objects[context.active_object.name]
    if 'armorpaint_filename' in objM:
        if os.path.isfile(objM["armorpaint_proj_dir"] + SEP + self["filename"]):
            objM["armorpaint_filename"] = self["filename"]
        else:
            self["filename"] = "ERROR: File not found"
    

class ArmorPaintLiveLinkProperties(PropertyGroup):

    project_path : StringProperty(
        name="ArmorPaint Project Directory",
        description="Path to ArmorPaint Project Directory",
        default="//",
        maxlen=1024,
        subtype='DIR_PATH')
    
    useCustomFilename : BoolProperty(
        name="Use custom filename",
        description="",
        default=False)
    
    filename : StringProperty(  
        name="ArmorPaint File name",
        description="File name",
        default="",
        update=update_filename)
        
    useCustomTextureDir : BoolProperty(
        name="Use custom texture dir",
        description="",
        default=False)
    
    texture_path : StringProperty(
        name="ArmorPaint Texture Directory",
        description="Texture directory",
        default= SEP +"exports" + SEP,
        maxlen=1024,
        subtype='DIR_PATH')

# ------------------------------------------------------------------------------
#    Addon Preferences
# ------------------------------------------------------------------------------

class ArmorPaintLiveLinkAddonPreferences(AddonPreferences):
    bl_idname = __name__

    path_exe: StringProperty(
            name="ArmorPaint Executable",
            subtype='FILE_PATH',
        )

    def draw(self, context):
        layout = self.layout

        if SYSTEM == "Windows":
            layout.label(text="Current OS: Windows")
            layout.label(text="Please select the location of " +
                                "the ArmorPaint.exe")
        elif SYSTEM == "Linux":
            layout.label(text="Current OS: Linux")
            layout.label(text="Please select this path: " +
            "\"ArmorPaint-Installation-Path/ArmorPaint\"")
        elif SYSTEM == "Darwin":
            layout.label(text="Current OS: MacOS")
            layout.label(text="Please select this path: " +
            "\"ArmorPaint-Installation-Path/ArmorPaint.app/Contents/MacOS/\"")
        layout.prop(self, "path_exe")
            
# ------------------------------------------------------------------------------
#    Addon Operators
# ------------------------------------------------------------------------------

class ArmorPaintLivelinkOperator(Operator):

    bl_idname = "object.armorpaint_livelink"
    bl_label = "Export Selection to ArmorPaint"
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        scn = context.scene
        Prefs = context.preferences.addons[__name__].preferences
        path_exe = Prefs.path_exe
        path_dir = dirname(Prefs.path_exe)
        
        typM = context.active_object.type
        objN = context.active_object.name
        objM = bpy.data.objects[objN]
        
        projP = scn.armorpaint_properties.project_path
        


        #ERRORS
        if typM != 'MESH':
            self.report({'ERROR'}, "ArmorPaint only works with Meshes!")
            return {'CANCELLED'}
        if path_exe == "":
            self.report({'ERROR'}, "No ArmorPaint executable path in settings")
            return {'CANCELLED'}
        if scn.armorpaint_properties == "":
            self.report({'ERROR'}, "Set an ArmorPaint Project directory please")
            return {'CANCELLED'}
        

        if 'armorpaint_proj_dir' in objM and \
            os.path.isfile(objM["armorpaint_proj_dir"] + SEP + objM["armorpaint_filename"]):
            # write the filePath of .arm file
            armFilepath = objM["armorpaint_proj_dir"] + SEP + objM["armorpaint_filename"]
            # Launch ArmorPaint with the last edit of the object
            subprocess.Popen([path_exe,armFilepath])
        else:
            # Generating Paths for each OS
            if SYSTEM == "Darwin":
                #Darwin need another path because you can't write inside of an application directory 
                path_tmp = os.path.expanduser("~") + SEP + "tmp.obj"
            else:
                path_tmp = path_dir + SEP + "data"+ SEP + "tmp.obj"
        
            # Export current object as obj and open it in armorpaint
            # Export the object as Obj and save it in the correct directory
            bpy.ops.export_scene.obj(filepath=path_tmp,
                                    check_existing=True,
                                    axis_forward='-Z',
                                    axis_up='Y',
                                    filter_glob="*.obj;*.mtl",
                                    use_selection=True,
                                    use_animation=False,
                                    use_mesh_modifiers=True,
                                    use_edges=True,
                                    use_smooth_groups=True,
                                    use_smooth_groups_bitflags=False,
                                    use_normals=True,
                                    use_uvs=True,
                                    use_materials=True,
                                    use_triangles=False,
                                    use_nurbs=False,
                                    use_vertex_groups=False,
                                    use_blen_objects=True,
                                    group_by_object=False,
                                    group_by_material=False,
                                    keep_vertex_order=False,
                                    global_scale=1,
                                    path_mode='AUTO')

            #Launch ArmorPaint
            subprocess.Popen([path_exe,path_tmp])
            
            objM["armorpaint_proj_dir"] = os.path.realpath(bpy.path.abspath(projP))
            objM["armorpaint_filename"] = str(objN) + ".arm"

        return {'FINISHED'}

class ArmorPaintLivelinkTexturesLoaderOperator(Operator):

    bl_idname = "object.armorpaint_livelink_textures_loader"
    bl_label = "ArmorPaint Live-Link - Load Textures"
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        scn = context.scene
        objM = bpy.data.objects[context.active_object.name]
        useCTD = scn.armorpaint_properties.useCustomTextureDir
        texP = scn.armorpaint_properties.texture_path

        if ( useCTD and os.path.isdir(texP)):
            generateMaterial(texP)
        else:
            generateMaterial(objM["armorpaint_proj_dir"] + SEP + "exports")

        return {'FINISHED'}

# ------------------------------------------------------------------------------
#    Addon GUI
# ------------------------------------------------------------------------------

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ArmorPaint"

    @classmethod
    def poll(cls, context):
        return context.object is not None

class ArmorPaintProjectFolder(View3DPanel, Panel):
    
    bl_idname = "VIEW3D_PT_armorpaint"
    bl_label = "ArmorPaint Live-link"
    
    def draw(self, context):
        scn = context.scene

        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Project Directory :")
        col.prop(scn.armorpaint_properties, 
                "project_path", 
                text="")

class ArmorPaintOpenPanel(View3DPanel, Panel):

    bl_idname = "VIEW3D_PT_armorpaint_open_panel"
    bl_label = "Open AmorPaint"

    def draw(self, context):
        scn = context.scene
        typM = context.active_object.type
        useCF = scn.armorpaint_properties.useCustomFilename
        
        layout = self.layout
        col = layout.split().column()
        
        if typM == 'MESH':
            col.prop(scn.armorpaint_properties, 
                    "useCustomFilename", 
                    text="Custom File Name")
            if(useCF):
                col.prop(scn.armorpaint_properties, 
                        "filename", 
                        text="")
            col.operator("object.armorpaint_livelink",
                        text="Open into ArmorPaint",
                        icon='TPAINT_HLT')
        else:
            col.label(icon='CANCEL',
                        text="Only meshes can be exported")

class ArmorPaintSyncTexturesPanel(View3DPanel, Panel):

    bl_idname = "VIEW3D_PT_armorpaint_import_textures"
    bl_label = "Sync Textures"

    def draw(self, context):
        scn = context.scene
        typM = context.object.type
        objM = bpy.data.objects[context.active_object.name]

        useCF = scn.armorpaint_properties.useCustomTextureDir
        texP = scn.armorpaint_properties.texture_path

        layout = self.layout
        col = layout.split().column()
        
        if typM == 'MESH':
            if "armorpaint_proj_dir" in objM and \
                os.path.isdir(objM["armorpaint_proj_dir"]):
                
                col.prop(scn.armorpaint_properties, 
                        "useCustomTextureDir", 
                        text="Custom Texture Directory")
                
                if(useCF):
                    col.prop(scn.armorpaint_properties, 
                            "texture_path", 
                            text="Directory")
                
                if(useCF and os.path.isdir(texP)):
                    exportDir = texP
                else:
                    exportDir = objM["armorpaint_proj_dir"] + SEP + "exports"
                
                if os.path.isdir(exportDir): 
                    col.operator("object.armorpaint_livelink_textures_loader",
                                text="Load textures",
                                icon='SHADING_TEXTURE')
                else: #Create exports directory
                    ttmp="Textures must be in a subdirectory called \"exports\""
                    col.label(text=ttmp)
            else:
                ttmp = "Open your mesh in ArmorPaint"
                col.label(text=ttmp)
                ttmp = " before applying textures please!"
                col.label(text=ttmp)
        else: 
            col.label(icon='CANCEL',
                    text="Only meshes support textures!")
    

# ------------------------------------------------------------------------------
#    Addon Register
# ------------------------------------------------------------------------------

classes = (
        ArmorPaintLiveLinkProperties,
        ArmorPaintLiveLinkAddonPreferences,
        ArmorPaintLivelinkOperator,
        ArmorPaintLivelinkTexturesLoaderOperator,
        ArmorPaintProjectFolder,
        ArmorPaintOpenPanel,
        ArmorPaintSyncTexturesPanel
    )

def register():
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.armorpaint_properties = PointerProperty(type=ArmorPaintLiveLinkProperties)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.armorpaint_properties


if __name__ == "__main__":
    register()
