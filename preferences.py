import bpy
from .icons_load import get_icon
from .export.funcs import get_author_from_printed_file, file_exists
from .export.operators import UnloadPrintedFile_OT_Operator

class InzoiderExtensionProperties(bpy.types.AddonPreferences):
    bl_idname = __package__

    my3dprinter_path : bpy.props.StringProperty(
        name="3DPrinter Path",
        description="Path to the inZOI's 3d prints directory",
        default="",
        subtype='DIR_PATH',
    )
    
    example_printed_file_path : bpy.props.StringProperty(
        name="printed.dat File",
        description="Path to the example printed file",
        default="",
        subtype='FILE_PATH',
    )
    
    detected_author : bpy.props.StringProperty(
        name="Detected Author",
        description="Detected author from the printed.dat file",
        default="",
    )
    
    is_printed_file_loaded : bpy.props.BoolProperty(
        name="Is Printed File Loaded",
        description="Whether the printed.dat file is loaded or not",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        self.is_printed_file_loaded = file_exists(self.example_printed_file_path)
        header, panel = layout.panel("inzoider_settings", default_closed=True)
        header.label(text="3D Prints", icon_value=get_icon("wall"))
        if panel:
            panel.prop(self, "my3dprinter_path", icon_value=get_icon("printer_3d"))
            if not self.is_printed_file_loaded:
                panel.prop(self, "example_printed_file_path", icon_value=get_icon("file_account_outline"))
                panel.label(text="No printed.dat file has been loaded, author not available", icon_value=get_icon("account_tie"))
            else:
                row_panel = panel.row(align=True)
                row_panel.alignment = 'CENTER'
                row_panel.label(text="Printed.dat file loaded", icon_value=get_icon("text_box_edit_outline"))
                self.detected_author = get_author_from_printed_file(self.example_printed_file_path) if self.is_printed_file_loaded else ""
                if self.detected_author:
                    row_panel.operator(UnloadPrintedFile_OT_Operator.bl_idname, text="", icon="PANEL_CLOSE")
                    row_panel.separator()
                    row_panel.label(text=f'Author: {self.detected_author}', icon_value=get_icon("account_tie"))
        

def get_addon_prefs() -> InzoiderExtensionProperties:
    return bpy.context.preferences.addons[__package__].preferences

def register():
    bpy.utils.register_class(InzoiderExtensionProperties)
    
def unregister():
    bpy.utils.unregister_class(InzoiderExtensionProperties)