# -*- coding: utf-8 -*-
# python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os

import bpy

def searchTextures(path):
    """Textures search functions.

    Args:
        path (str): Texture folder

    Returns:
        list: str : List of texture paths
    """
    textures = [None,
    None,
    None,
    None,
    None,
    None,
    None]

    dir = os.listdir(path)
    for f in dir:
        if(os.path.isfile(os.path.join(path, f))
            and f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.hdr', '.exr'))):
            # TODO: Try the new case function of Python 3.10+
            if(f.find("_base") > 1): textures[0] = os.path.join(path, f)
            if(f.find("_subs") > 1): textures[1] = os.path.join(path, f)
            if(f.find("_metal") > 1): textures[2] = os.path.join(path, f)
            if(f.find("_rough") > 1): textures[3] = os.path.join(path, f)
            if(f.find("_emission") > 1): textures[4] = os.path.join(path, f)
            if(f.find("_opac") > 1): textures[5] = os.path.join(path, f)
            if(f.find("_nor") > 1): textures[6] = os.path.join(path, f)
    return textures

def reloadTextures():
    """Reload textures already stored inside of Blender.
    """
    # Clean up unused images
    for img in bpy.data.images:
        if not img.users:
            bpy.data.images.remove(img)

    #Reload all File images
    for img in bpy.data.images :
        if img.source == 'FILE' :
            img.reload()

def generateMaterial(path):
    """Generate the node tree for textures.
    TODO: Update this function with a more pythonic approch.

    Args:
        path (str): Path to texture directory
    """
    textures = [
        None, # basecolor
        None, # subsurf
        None, # metal
        None, # rough
        None, # emission
        None, # opac
        None  # normalmap
    ]
    
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

class ArmorPaintLivelinkTexturesLoaderOperator(bpy.types.Operator):
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
            generateMaterial(os.path.join(objM["armorpaint_proj_dir"], "exports"))

        return {'FINISHED'}