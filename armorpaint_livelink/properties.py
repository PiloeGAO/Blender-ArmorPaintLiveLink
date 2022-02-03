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
from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty

def update_filename(self, context):
    """Function used to setup the filename.

    Args:
        context ([type]): [description]
    """
    if not self["filename"].endswith(".arm") and self["filename"] != "":
        self["filename"] += ".arm"
    
    objM = bpy.data.objects[context.active_object.name]
    if 'armorpaint_filename' in objM:
        if os.path.isfile(os.path.join(objM["armorpaint_proj_dir"], self["filename"])):
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
        default= "/exports/",
        maxlen=1024,
        subtype='DIR_PATH')