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
import platform

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

SYSTEM = platform.system()

addonName = os.path.basename(os.path.dirname(__file__))

class ArmorPaintLiveLinkAddonPreferences(AddonPreferences):
    bl_idname = addonName

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

def getPreferences():
    """Get addon preferences.
    Sources: https://github.com/JacquesLucke/animation_nodes/blob/master/animation_nodes/preferences.py

    Returns:
        :obj:`AddonPreferences`: Preference of the Addon
    """
    return bpy.context.preferences.addons[addonName].preferences