import bpy
from .funcs import change_selection
from .constants import CRAFT_TYPES

class CraftItem(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(name="Type", items=CRAFT_TYPES)
    mesh: bpy.props.PointerProperty(name="Mesh", type=bpy.types.Object)
    thumbnail: bpy.props.PointerProperty(name="Thumbnail", type=bpy.types.Image)
    title: bpy.props.StringProperty(name="Title", default="")
    description: bpy.props.StringProperty(name="Description", default="")
    enable_editing: bpy.props.BoolProperty(name="Enable Editing", default=False, description="Enable editing of the craft's properties")
    
def register():
    bpy.types.Scene.obj_craft_list = bpy.props.CollectionProperty(type=CraftItem)
    bpy.types.Scene.obj_craft_index = bpy.props.IntProperty(name="Craft", default=0, description="Index of the selected craft", update=change_selection)
    bpy.types.Scene.inzoider_export_all = bpy.props.BoolProperty(name="Export All", default=False, description="Export all crafts in the list")
    bpy.types.WindowManager.current_craft_image_path = bpy.props.StringProperty()
    bpy.types.WindowManager.current_craft_texture_name = bpy.props.StringProperty()
    
def unregister():
    del bpy.types.Scene.obj_craft_list
    del bpy.types.Scene.obj_craft_index
    del bpy.types.Scene.inzoider_export_all
    del bpy.types.WindowManager.current_craft_image_path
    del bpy.types.WindowManager.current_craft_texture_name