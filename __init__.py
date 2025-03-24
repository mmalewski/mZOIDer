def reload_inzoider():
    import sys
    print("Reloading Inzoider")
    
    
    global auto_load
    del auto_load
    inzoider_module_prefix = f"{__package__}."
    module_names = list(sys.modules.keys())
    for name in module_names:
        if name.startswith(inzoider_module_prefix):
            del sys.modules[name]
            
if "auto_load" in locals():
    reload_inzoider()

from . import icons_load
from . import auto_load

auto_load.init()

def register():
    icons_load.init_icons()
    icons_load.load_icons()
    auto_load.register()

def unregister():
    auto_load.unregister()
    icons_load.unregister_icons()