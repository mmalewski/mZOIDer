import bpy

class CraftItem(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(name="Type", items=[
        ('Build', "Build", "Build"),
        ('Character', "Character", "Character"),
    ])
    mesh: bpy.props.PointerProperty(name="Mesh", type=bpy.types.Object)
    thumbnail: bpy.props.PointerProperty(name="Thumbnail", type=bpy.types.Image)
    title: bpy.props.StringProperty(name="Title", default="")
    description: bpy.props.StringProperty(name="Description", default="")
    author: bpy.props.StringProperty(name="Author", default="")
    
def register():
    bpy.types.Scene.obj_craft_list = bpy.props.CollectionProperty(type=CraftItem)
    bpy.types.Scene.obj_craft_index = bpy.props.IntProperty(name="Index", default=0)
    bpy.types.Scene.inzoi_3d_crafts_path = bpy.props.StringProperty(name="Inzoi 3D Crafts Path", default="", subtype='DIR_PATH')
    bpy.types.WindowManager.current_craft_image_path = bpy.props.StringProperty()
    bpy.types.WindowManager.current_craft_texture_name = bpy.props.StringProperty()
    
def unregister():
    del bpy.types.Scene.obj_craft_list
    del bpy.types.Scene.obj_craft_index
    del bpy.types.Scene.inzoi_3d_crafts_path
    del bpy.types.WindowManager.current_craft_image_path
    del bpy.types.WindowManager.current_craft_texture_name