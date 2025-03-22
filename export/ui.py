import bpy
from .operators import FakeOperator_OT_Operator, AddCraftItem_OT_Operator, ExportCraft_OT_Operator, RemoveCraftItem_OT_Operator


class CRAFT_UL_list(bpy.types.UIList):
    bl_idname = "CRAFT_UL_list"
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = context.scene
        row = layout.row()
        row.label(text=f"{item.title} by {item.author}", icon='GHOST_ENABLED')
        match item.type:
            case 'Build':
                row.label(text="Build", icon='MESH_CUBE')
            case 'Character':
                row.label(text="Character", icon='ARMATURE_DATA')


class InzoiderCraftExport_PT_Panel(bpy.types.Panel):
    bl_label = "Craft Export"
    bl_idname = "InzoiderCraftExport_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Inzoider'
    bl_options = {'DEFAULT_CLOSED'}
        
    def draw_header(self, context):
        self.layout.label(text="", icon='FCURVE_SNAPSHOT')
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.operator(AddCraftItem_OT_Operator.bl_idname, text="", icon='ADD')
        col.operator(RemoveCraftItem_OT_Operator.bl_idname, text="", icon='REMOVE')
        col.separator()
        col.operator(ExportCraft_OT_Operator.bl_idname, text="", icon='EXPORT')
        col.separator()
        row = row.row()
        col = row.column(align=False)
        col.scale_x = 1.2
        col.template_list(CRAFT_UL_list.bl_idname, "", scene, "obj_craft_list", scene, "obj_craft_index")
        col.prop(scene, "inzoi_3d_crafts_path", text="inZOI ImageTo3D Path", icon='FILE_FOLDER', expand=True)
        
        selected_item = scene.obj_craft_list[scene.obj_craft_index] if scene.obj_craft_list else None
        
        if selected_item:
            header, panel = layout.panel("_item details")
            header.label(text="Details", icon='MOD_VERTEX_WEIGHT')
            row_panel = panel.row()
            col_panel = row_panel.column()
            
            col_panel.prop(selected_item, "title")
            col_panel.prop(selected_item, "description")
            col_panel.prop(selected_item, "author")
            col_panel.prop(selected_item, "type")
            col_panel.prop(selected_item, "thumbnail")
            col_panel.enabled = False
            col_panel.prop(selected_item, "mesh", text="Linked Object")