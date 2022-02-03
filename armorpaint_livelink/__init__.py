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
from . import auto_load

bl_info = {
    "name" : "ArmorPaint LiveLink",
    "author" : "Leo Depoix - PiloeGAO",
    "version": (1, 1, 0),
    "blender": (2, 83, 0),
    "location": "3D View > Side Bar",
    "description": "Integration of ArmorPaint into Blender Workflow",
    "warning": "Development",
    "wiki_url": "https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink",
    "tracker_url": "https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink/issues",
    "category": "Paint"
}

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()