import bpy
from .operators import FakeOperator_OT_Operator, add_craft_item_OT_Operator


class CRAFT_UL_list(bpy.types.UIList):
    bl_idname = "CRAFT_UL_list"
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = context.scene
        layout.label(text="Hola")
        #show image


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
        col.operator(add_craft_item_OT_Operator.bl_idname, text="", icon='ADD')
        col.operator(FakeOperator_OT_Operator.bl_idname, text="", icon='REMOVE')
        col.separator()
        col.operator(FakeOperator_OT_Operator.bl_idname, text="", icon='EXPORT')
        col.separator()
        row = row.row()
        col = row.column(align=False)
        col.scale_x = 1.2
        col.template_list(CRAFT_UL_list.bl_idname, "", scene, "obj_craft_list", scene, "obj_craft_index")
    