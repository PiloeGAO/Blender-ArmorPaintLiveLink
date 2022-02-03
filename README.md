# Blender ArmorPaint Livelink

*The project is not under active development, fix updates are made as soon as possible (please consider [donating](https://github.com/PiloeGAO/Blender-ArmorPaintLiveLink#Donation) for faster updates)*

This addon is the current implementation of live link for [ArmorPaint](http://www.armorpaint.org) inside of Blender 2.8+

![](addon_properties.png)  

**Figure 1** - Addon Properties  

![](UI.png)  

**Figure 2** - Addon tab in the 3D View  

## Getting Started

### Prerequisites

Download latest version of Blender (v. 2.80 minimum) and ArmorPaint V0.8.

### Installing

1. Clone the repository  
2. Inside of Blender, *Edit > Preferences... > Add-ons (Tab) > install..* the armorpaint_livelink.py file  
3. Turn on the addon  
4. Add the ArmorPaint executable path in the "ArmorPaint Executable" field  
5. In the 3D View, open the panel side (*N* shortcut) and locate the project directory  (folder where your Arm file and textures will be saved)  
6. Select your object  (he needs to be unwrapped) and click on the "Open in ArmorPaint" to edit it inside of ArmorPaint  (* Optionnal:You can use a custom arm name instead of the object name - example: Use "MyBeautifullCube.arm" for the "Cube" object instead of "Cube.arm"*)  
7. When the texturing process is done, export your textures to a subdirectory called "exports" (* Optionnal: You can also use a custom directory for your textures - example: "/highdefTextures/"*)

## Feature Request

Your project as a special needed?

Please add your request in "Issues", we will looking for it as fast as possible!

## Contributing

Contributions are encouraged, but the code need to stay clear and organized.
Also, fixes for self-compiled versions are not allowed, we only target ArmorPaint official builds for now.

## Authors

* **[PiloeGAO](https://github.com/PiloeGAO)** - *Initial work*
* **[Spirou4D](https://github.com/Spirou4D)** - *Code fix*
* **[tobiasBora](https://github.com/tobiasBora)** - *Temporary directory fix*

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details.

## Donation

You can support this project by making a donation.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=VXD77HL4GZNP6)
