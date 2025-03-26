import bpy
from .funcs import get_obj_extents, create_printed_file, generate_md5_from_str, current_time_str, convert_image_to_jpg, create_folder, export_obj_as_glb, change_visual_rotation_to_obj
from .meta import Meta
from ..icons_load import get_icon
from .constants import CRAFT_TYPES

class SelectImage_OT_Operator(bpy.types.Operator):
    """Select an image to use as the thumbnail for the craft item"""
    bl_idname = "inzoider.select_image_for_craft"
    bl_label = "Select Image"
    
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default="")
    filter_glob: bpy.props.StringProperty(default='*.jpg;*.jpeg;*.png', options={'HIDDEN'})
    
    def execute(self, context):
        context.window_manager.current_craft_image_path = self.filepath
        
        try:
            img = bpy.data.images.load(self.filepath, check_existing=True)
            img.colorspace_settings.name = 'sRGB'
            texture_name = f"thumb_{bpy.path.basename(self.filepath).split('.')[0]}"
            
            if texture_name in bpy.data.textures:
                tex = bpy.data.textures[texture_name]
            else:
                tex = bpy.data.textures.new(name=texture_name, type='IMAGE')
                
            tex.image = img
            
            tex.extension = 'CLIP'
            
            tex.crop_min_x = -0.75
            tex.crop_min_y = 0.0
            
            tex.crop_max_x = 0.25
            tex.crop_max_y = 1.0
            
            context.window_manager.current_craft_texture_name = texture_name
            
            
        except Exception as e:
            self.report({'ERROR'}, f"Could not load image: {str(e)}")
            print(f"Error loading image: {str(e)}")
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class AddCraftItem_OT_Operator(bpy.types.Operator):
    """Add a new craft item to the list"""
    bl_idname = "inzoider.add_craft_item"
    bl_label = "Add Craft Item"
    
    craft_title: bpy.props.StringProperty(name="Title", default="")
    craft_description: bpy.props.StringProperty(name="Description", default="", subtype='NONE')
    craft_use_obj_name_as_title: bpy.props.BoolProperty(name="Use Object Name as Title", default=False, description="Use the name of the selected object as the title instead of a custom one")
    craft_author: bpy.props.StringProperty(name="Author", default="")
    craft_type: bpy.props.EnumProperty(name="Type", items=CRAFT_TYPES, default='Build')
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) == 1 and context.selected_objects[0].type == 'MESH'
    
    def invoke(self, context, event):
        context.window_manager.current_craft_image_path = ""
        context.window_manager.current_craft_texture_name = ""
        self.craft_title = ""
        self.craft_description = ""
        self.craft_author = ""
        self.craft_type = 'Build'
        return context.window_manager.invoke_props_dialog(self, title="Craft Properties", width=400)
            
    def execute(self, context):
        
        if self.craft_title == "":
            self.report({'ERROR'}, "Please enter a title for the craft item")
            return {'CANCELLED'}
        
        if self.craft_description == "":
            self.report({'ERROR'}, "Please enter a description for the craft item")
            return {'CANCELLED'}
        
        if self.craft_author == "":
            self.report({'ERROR'}, "Please enter an author for the craft item")
            return {'CANCELLED'}
        
        scene = context.scene
        item = scene.obj_craft_list.add()
        
        if self.craft_use_obj_name_as_title:
            item.title = context.active_object.name
        else:
            item.title = self.craft_title
            
        item.description = self.craft_description
        item.author = self.craft_author
        item.mesh = context.selected_objects[0]
        item.type = self.craft_type
        
        if context.window_manager.current_craft_texture_name:
            tex_name = context.window_manager.current_craft_texture_name
            if tex_name in bpy.data.textures:
                item.thumbnail = bpy.data.textures[tex_name].image
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(self, "craft_use_obj_name_as_title")
        if self.craft_use_obj_name_as_title:
            layout.label(text=f"Title: {context.active_object.name}", icon_value=get_icon("format_title"))
        else:
            layout.prop(self, "craft_title", icon_value=get_icon("format_title"))
            
        layout.prop(self, "craft_description", icon_value=get_icon("text_long"), expand=True)
        layout.prop(self, "craft_author", icon_value=get_icon("account_tie"))
        layout.prop(self, "craft_type", expand=True)
        box = layout.box()
        box.label(text="Thumbnail", icon_value=get_icon("image_frame"))
        
        box.operator(SelectImage_OT_Operator.bl_idname, text="Select")
        
        if context.window_manager.current_craft_texture_name:
            tex_name = context.window_manager.current_craft_texture_name
            if tex_name in bpy.data.textures:
                box.template_preview(bpy.data.textures[tex_name], show_buttons=False)
            else:
                box.label(text=f"Texture '{tex_name}' not found")
                
class RemoveCraftItem_OT_Operator(bpy.types.Operator):
    """Remove the selected craft item from the list"""
    bl_idname = "inzoider.remove_craft_item"
    bl_label = "Remove Craft Item"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.obj_craft_list) > 0
    
    def execute(self, context):
        scene = context.scene
        scene.obj_craft_list.remove(scene.obj_craft_index)
        scene.obj_craft_index = min(max(0, scene.obj_craft_index - 1), len(scene.obj_craft_list) - 1)
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event, title="Item Removal", icon='QUESTION', message="Are you sure you want to remove this item?")
            
class FakeOperator_OT_Operator(bpy.types.Operator):
    bl_idname = "fake.operator"
    bl_label = "Fake Operator"

    def execute(self, context):
        return {'FINISHED'}
    
class ExportCraft_OT_Operator(bpy.types.Operator):
    """Export the selected craft item to the Inzoi 3D Crafts folder"""
    bl_idname = "inzoider.export_craft"
    bl_label = "Export Craft"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.inzoider_export_all:
            return len(scene.obj_craft_list) > 0
        else:
            return len(scene.obj_craft_list) > 0 and scene.obj_craft_list[0].mesh is not None
    
    def execute(self, context):
        scene = context.scene
        selected_index = scene.obj_craft_index
        items = scene.obj_craft_list if scene.inzoider_export_all else [scene.obj_craft_list[selected_index]]
        
        if not scene.inzoider_3d_crafts_path:
            self.report({'ERROR'}, "Please set the Inzoi's ImageTo3D path.")
            return {'CANCELLED'}
        
        if items:
            for item in items:
                hash_name = generate_md5_from_str(f"{item.title}{current_time_str()}")
                new_folder = create_folder(scene.inzoider_3d_crafts_path + f"/{hash_name}")
                if item.type == 'Character':
                    #change_visual_rotation_to_obj(item.mesh, True)
                    print("This is a character")
                    change_visual_rotation_to_obj(item.mesh, True)
                    export_obj_as_glb(item.mesh, new_folder, hash_name.upper())
                    change_visual_rotation_to_obj(item.mesh, False)
                else:
                    export_obj_as_glb(item.mesh, new_folder, hash_name.upper())
                if item.thumbnail:
                    convert_image_to_jpg(new_folder, item.thumbnail)
                
                meta = Meta(
                    [0, 0, 0],
                    [0, 0, 0] if item.type == 'Character' else [0, -90, 0],
                    get_obj_extents(item.mesh),
                    item.title,
                    item.description,
                )
                meta.export_to_file(f"{new_folder}/meta.json")
                create_printed_file(item.author, new_folder)
                self.report({'INFO'}, f"Craft '{item.title}' exported successfully!")
        
        return {'FINISHED'}