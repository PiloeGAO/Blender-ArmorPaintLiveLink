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
    "name": "ArmorPaint Live-link",
    "author": "PiloeGAO (Leo DEPOIX)",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar",
    "description": "Integration of ArmorPaint into Blender Workflow",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Paint"}

import bpy
from bpy.types import Operator, AddonPreferences, WindowManager
from bpy.props import StringProperty, IntProperty, BoolProperty

import os, subprocess, platform

class ArmorPaintLiveLinkAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    path_base: StringProperty(
        name="ArmorPaint Path",
        subtype='FILE_PATH',
    )

    use_custom_project_path: BoolProperty(
        name="Use Custom Project Path",
        default=False,
    )

    custom_project_dir = StringProperty(
        name="Project Folder Path",
        subtype='DIR_PATH',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        
        if platform.system() == "Windows":
            layout.label(text="Current OS: Windows")
            layout.label(text="Note: Please select the directory of ArmorPaint")
        elif platform.system() == "Linux":
            layout.label(text="Current OS: Linux")
        elif platform.system() == "Darwin":
            layout.label(text="Current OS: MacOS")
            layout.label(text="Note: Please select this path: \"ArmorPaint-Installation-Path/ArmorPaint.app/Contents/MacOS/\"")
        layout.prop(self, "path_base")

        layout.label(text="By default, the addon use the place where the blend file is saved to open ArmorPaint files.")

        layout.prop(self, "use_custom_project_path")
        if self.use_custom_project_path == True: layout.prop(self, "custom_project_dir")

class ArmorPaintLivelinkOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.armorpaint_livelink"
    bl_label = "ArmorPaint Live-Link"

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        #Check if the object selected is currently a Mesh
        if bpy.context.object.type != 'MESH':
            self.report({'ERROR'}, "ArmorPaint only works wih Meshes!")
            return {'CANCELLED'}
        
        path_base = addon_prefs.path_base
        #Generating Paths for each OS
        if platform.system() == "Windows":
            path_tmp = path_base + "\\data\\tmp.obj"
            path_exe = path_base + "\\ArmorPaint.exe"
        elif platform.system() == "Linux":
            path_tmp = path_base + "/data/tmp.obj"
            path_exe = path_base + "/ArmorPaint"
        elif platform.system() == "Darwin":
            path_tmp = path_base + "/data/tmp.obj"
            path_exe = path_base + "/ArmorPaint"
        else:
            self.report({'ERROR'}, "System not found.")
            return {'CANCELLED'}
        
        if addon_prefs.custom_project_dir != " " and addon_prefs.use_custom_project_path:
            project_path = addon_prefs.custom_project_dir
        else:
            project_path = bpy.path.abspath("//")
        
        
        
        if 'armorpaint' in bpy.data.objects[bpy.context.active_object.name] and os.path.isfile(bpy.data.objects[bpy.context.active_object.name]["armorpaint"]):
            #Launch ArmorPaint with the last edit of the object
            subprocess.Popen([path_exe,bpy.data.objects[bpy.context.active_object.name]["armorpaint"]])

        else:
            #Export current object as obj and open it in armorpaint
            #Export the object as Obj and save it in the correct directory
            bpy.ops.export_scene.obj(filepath=path_tmp, check_existing=True, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl", use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=True, use_smooth_groups_bitflags=False, use_normals=True, use_uvs=True, use_materials=True, use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=1, path_mode='AUTO')
        
            #Launch ArmorPaint
            subprocess.Popen([path_exe,path_tmp])
            #adding custom value to the object
            bpy.data.objects[bpy.context.active_object.name]["armorpaint"] = project_path + "/" + str(bpy.context.active_object.name) + ".arm"
        
        return {'FINISHED'}

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ArmorPaint"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class ArmorPaintOpenPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_armorpaint_open_panel"
    bl_label = "Open AmorPaint"

    def draw(self, context):
        layout = self.layout
        if context.preferences.addons[__name__].preferences.path_base == "":
            layout.label(text="Select folder where ArmorPaint is located in Addon Preferences")
        else:
            split = layout.split()
            col = split.column()
            col.operator("object.armorpaint_livelink", text="Paint Selected", icon='TPAINT_HLT')
            warning_text= "Warning: You should save the ArmorPaint project with your object name; Here: " + str(bpy.context.active_object.name) + ".arm"
            layout.label(text=warning_text)


class ArmorPaintSyncTexturesPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_armorpaint_import_textures"
    bl_label = "Sync Textures"

    def draw(self, context):
        layout = self.layout
        layout.label(text="At this state of developement, you need to open your exported textures with the node Wrangler")

classes = (
    ArmorPaintLiveLinkAddonPreferences,
    ArmorPaintLivelinkOperator,
    ArmorPaintOpenPanel,
    ArmorPaintSyncTexturesPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
