# mZoider Extension for mZOI

### Transform your Blender creations into custom 3D prints for mZOI

![Inzoider Extension Preview](https://github.com/user-attachments/assets/13ec951a-6687-43ca-b90a-712f35bfd40d)

## [⬇️ Download Latest Release](https://github.com/mmalewski/mzoider/releases/latest)

## Requirements
- mZOI game
- Blender 4.2+
- 3D modelling and general Blender knowledge.

## Installation
1. Download the extension:
   - Get the latest release from the `Tags` section (Recommended)
2. Open Blender and navigate to `Edit > Preferences... > Add-ons`
3. Click the top-right arrow button and select `Install from Disk...`
4. Locate and select the downloaded ZIP file
5. Enable the add-on by checking its box in the list

## How to Use

### Setup
1. In the add-on preferences, set the 3D Printer path to:
   ```
   C:\Users\%USERNAME%\Documents\mZOI\AIGenerated\My3DPrinter
   ```
   > ℹ️ **Information:** `%USERNAME%` refers to your own Windows' username.
2. Generate at least one 3D print from mZOI
3. The add-on will use these files as templates for your custom creations
4. Select a ```printed.dat``` file from the previous path and load it.

### Exporting a Model
1. Prepare your 3D model in Blender:
   - Model or Download your model.
   - Apply textures to your object.
   - Ensure uniform scale `(1,1,1)` and rotation `(0,0,0)` (apply both if needed)
   - Set an proper pivot for your model. For example, if you are making a sofa, the pivot should be in the lower-middlemost part of the model.
3. Select your object in the scene
4. Open the side panel with the `N` key
5. Navigate to the "Inzoider" tab
6. Create a new craft by clicking the `+` button
7. Fill out all required fields
8. Select your craft from the list
9. Click "Export"
10. Launch mZOI to see your creation in-game

> ⚠️ **Note:** This tool is still experimental. Please report any issues you encounter.
