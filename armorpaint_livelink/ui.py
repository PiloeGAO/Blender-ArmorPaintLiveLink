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
from bpy.types import Panel

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
                    exportDir = os.path.join(objM["armorpaint_proj_dir"], "exports")
                
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