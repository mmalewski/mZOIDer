import bpy
import os
from bpy.utils import previews

pcoll = None
preview_collections = {}

def init_icons():
    """Initializes the icon collections."""
    global pcoll, preview_collections
    if preview_collections:
        for coll in preview_collections.values():
            bpy.utils.previews.remove(coll)
        preview_collections.clear()
    
    pcoll = previews.new()
    preview_collections["main"] = pcoll
    return pcoll

def ensure_icons_loaded():
    """Checks if the icons are loaded, and if not, loads them."""
    global pcoll, preview_collections
    if pcoll is None or not preview_collections.get("main"):
        init_icons()
        load_icons()
    return pcoll

def load_icons():
    """Loads all custom icons."""
    global pcoll
    
    if pcoll is None:
        init_icons()
    
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    print(f"Loading icons from: {icons_dir}")
    
    icons = [
        ["account_tie", "account_tie.png"],
        ["coffee", "coffee.png"],
        ["cube", "cube.png"],
        ["export", "export.png"],
        ["format_title", "format_title.png"],
        ["github", "github.png"],
        ["image_frame", "image_frame.png"],
        ["printer_3d", "printer_3d.png"],
        ["sofa_outline", "sofa_outline.png"],
        ["table_furniture", "table_furniture.png"],
        ["text_box_edit_outline", "text_box_edit_outline.png"],
        ["text_long", "text_long.png"],
        ["wall", "wall.png"],
        ["hanger", "hanger.png"],
        ["format_list_bulleted_type", "format_list_bulleted_type.png"],
        ["file_account_outline", "file_account_outline.png"],
    ]
    
    for name, filename in icons:
        if name in pcoll:
            print(f"Icon '{name}' already exists, skipping")
            continue
            
        icon_path = os.path.join(icons_dir, filename)
        if os.path.exists(icon_path):
            pcoll.load(name, icon_path, 'IMAGE')
        else:
            print(f"Icon not found: {icon_path}")
    
    print(f"Loaded icons: {list(pcoll.keys())}")
    return pcoll

def get_icon(icon_name, fallback="QUESTION"):
    """Safely obtains an icon ID."""
    global pcoll
    ensure_icons_loaded()
    try:
        return pcoll[icon_name].icon_id
    except (KeyError, AttributeError):
        print(f"Warning: Icon '{icon_name}' not found, using fallback")
        return fallback

def unregister_icons():
    """Removes all icon collections."""
    global pcoll, preview_collections
    for coll in preview_collections.values():
        bpy.utils.previews.remove(coll)
    preview_collections.clear()
    pcoll = None