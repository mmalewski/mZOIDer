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

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()