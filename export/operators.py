import bpy
from .funcs import get_obj_extents, create_printed_file, generate_md5_from_str, current_time_str, convert_image_to_jpg, create_folder, export_obj_as_glb
from .meta import Meta

class SelectImage_OT_Operator(bpy.types.Operator):
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
    bl_idname = "inzoider.add_craft_item"
    bl_label = "Add Craft Item"
    
    craft_title: bpy.props.StringProperty(name="Title", default="")
    craft_description: bpy.props.StringProperty(name="Description", default="", subtype='NONE', options={'TEXTEDIT_UPDATE'})
    craft_use_obj_name_as_title: bpy.props.BoolProperty(name="Use Object Name as Title", default=False, description="Use the name of the selected object as the title instead of a custom one")
    craft_author: bpy.props.StringProperty(name="Author", default="")
    craft_type: bpy.props.EnumProperty(name="Type", items=[
        ('Build', "Build", "Build", "MOD_BUILD", 0),
        ('Character', "Character", "Character", "ARMATURE_DATA", 1),])
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) == 1 and context.selected_objects[0].type == 'MESH'
    
    def invoke(self, context, event):
        context.window_manager.current_craft_image_path = ""
        context.window_manager.current_craft_texture_name = ""
        return context.window_manager.invoke_props_dialog(self, title="Craft Properties", width=400)
            
    def execute(self, context):
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
            layout.label(text=f"Title: {context.active_object.name}")
        else:
            layout.prop(self, "craft_title")
            
        layout.prop(self, "craft_description")
        layout.prop(self, "craft_author")
        layout.prop(self, "craft_type")
        box = layout.box()
        box.label(text="Thumbnail Image:")
        
        box.operator(SelectImage_OT_Operator.bl_idname, text="Select Image", icon='FILE_IMAGE')
        
        if context.window_manager.current_craft_texture_name:
            tex_name = context.window_manager.current_craft_texture_name
            if tex_name in bpy.data.textures:
                box.template_preview(bpy.data.textures[tex_name], show_buttons=False)
            else:
                box.label(text=f"Texture '{tex_name}' not found")
                
class RemoveCraftItem_OT_Operator(bpy.types.Operator):
    bl_idname = "inzoider.remove_craft_item"
    bl_label = "Remove Craft Item"
    
    def execute(self, context):
        scene = context.scene
        scene.obj_craft_list.remove(scene.obj_craft_index)
        scene.obj_craft_index = min(max(0, scene.obj_craft_index - 1), len(scene.obj_craft_list) - 1)
        return {'FINISHED'}
            
class FakeOperator_OT_Operator(bpy.types.Operator):
    bl_idname = "fake.operator"
    bl_label = "Fake Operator"

    def execute(self, context):
        return {'FINISHED'}
    
class ExportCraft_OT_Operator(bpy.types.Operator):
    bl_idname = "inzoider.export_craft"
    bl_label = "Export Craft"
    
    def execute(self, context):
        scene = context.scene
        item = scene.obj_craft_list[scene.obj_craft_index]
        
        if item:
            meta = Meta(
                [0, 0, 0],
                [0, 0, 0] if item.type == 'Character' else [0, -90, 0],
                get_obj_extents(item.mesh),
                item.title,
                item.description,
            )
            
            hash_name = generate_md5_from_str(f"{item.title}{current_time_str()}")
            new_folder = create_folder(scene.inzoi_3d_crafts_path + f"/{hash_name}")
            
            meta.export_to_file(f"{new_folder}/meta.json")
            create_printed_file(item.author, new_folder)
            
            export_obj_as_glb(item.mesh, new_folder, hash_name.upper())
            if item.thumbnail:
                convert_image_to_jpg(new_folder, item.thumbnail)
            
            
            
            self.report({'INFO'}, f"Craft '{item.title}' exported successfully!")
        
        return {'FINISHED'}