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
import subprocess
import tempfile

import bpy

from .. preferences import getPreferences

class ArmorPaintLivelinkOperator(bpy.types.Operator):
    bl_idname = "object.armorpaint_livelink"
    bl_label = "Export Selection to ArmorPaint"
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        scn = context.scene
        Prefs = getPreferences()
        path_exe = Prefs.path_exe
        
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
            os.path.isfile(os.path.join(objM["armorpaint_proj_dir"], objM["armorpaint_filename"])):
            # write the filePath of .arm file
            armFilepath = os.path.join(objM["armorpaint_proj_dir"], objM["armorpaint_filename"])
            # Launch ArmorPaint with the last edit of the object
            subprocess.Popen([path_exe, armFilepath])
        else:
            # Create a temporary file to store the .obj
            path_tmp = tempfile.mkstemp(suffix=".obj")[1]
        
            # Export current object as obj and open it in armorpaint
            # Export the object as Obj and save it in the correct directory
            bpy.ops.export_scene.obj(
                filepath=path_tmp,
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
                path_mode='AUTO'
            )

            #Launch ArmorPaint
            subprocess.Popen([path_exe,path_tmp])
            
            objM["armorpaint_proj_dir"] = os.path.realpath(bpy.path.abspath(projP))
            objM["armorpaint_filename"] = str(objN) + ".arm"

        return {'FINISHED'}