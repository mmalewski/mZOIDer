import bpy
from .icons_load import get_icon

class InzoiderExtensionProperties(bpy.types.AddonPreferences):
    bl_idname = __package__

    inzoi_my3dprinter_path : bpy.props.StringProperty(
        name="3DPrinter Path",
        description="Path to the inzoi's 3d prints directory",
        default="",
        subtype='DIR_PATH',
    )
    
    inzoi_example_printed_file_path : bpy.props.StringProperty(
        name="printed.dat File",
        description="Path to the example printed file",
        default="",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        header, panel = layout.panel("inzoider_settings", default_closed=True)
        header.label(text="Inzoider Settings", icon_value=get_icon("wall"))
        if panel:
            panel.prop(self, "inzoi_my3dprinter_path", icon_value=get_icon("printer_3d"))
            panel.prop(self, "inzoi_example_printed_file_path", icon_value=get_icon("file_account_outline"))
        

def get_addon_prefs() -> InzoiderExtensionProperties:
    return bpy.context.preferences.addons[__package__].preferences

def register():
    bpy.utils.register_class(InzoiderExtensionProperties)
    
def unregister():
    bpy.utils.unregister_class(InzoiderExtensionProperties)