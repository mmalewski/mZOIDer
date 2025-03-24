import bpy
from .funcs import update_path
from .constants import CRAFT_TYPES

class CraftItem(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(name="Type", items=CRAFT_TYPES)
    mesh: bpy.props.PointerProperty(name="Mesh", type=bpy.types.Object)
    thumbnail: bpy.props.PointerProperty(name="Thumbnail", type=bpy.types.Image)
    title: bpy.props.StringProperty(name="Title", default="")
    description: bpy.props.StringProperty(name="Description", default="")
    author: bpy.props.StringProperty(name="Author", default="")
    enable_editing: bpy.props.BoolProperty(name="Enable Editing", default=False)
    
def register():
    bpy.types.Scene.obj_craft_list = bpy.props.CollectionProperty(type=CraftItem)
    bpy.types.Scene.obj_craft_index = bpy.props.IntProperty(name="Index", default=0)
    bpy.types.Scene.inzoi_3d_crafts_path = bpy.props.StringProperty(name="Inzoi 3D Crafts Path", default="", subtype='DIR_PATH', update=update_path)
    bpy.types.WindowManager.current_craft_image_path = bpy.props.StringProperty()
    bpy.types.WindowManager.current_craft_texture_name = bpy.props.StringProperty()
    
def unregister():
    del bpy.types.Scene.obj_craft_list
    del bpy.types.Scene.obj_craft_index
    del bpy.types.Scene.inzoi_3d_crafts_path
    del bpy.types.WindowManager.current_craft_image_path
    del bpy.types.WindowManager.current_craft_texture_name