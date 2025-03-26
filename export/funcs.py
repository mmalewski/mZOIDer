from bpy.types import Object, Image
import hashlib
import bpy
from math import radians
import os
import time


def get_obj_extents(obj: Object) -> tuple:
    """Gets proper extents of object to match inZOI scale."""
    return list(obj.dimensions * 50)

def create_printed_file(author: str, file_path: str) -> None:
    """Creates a printed.dat file."""
    with open(f"{file_path}/printed.dat", 'wb+') as file:
        file.write(b'\x01\x00\x00\x00\x25\x00\x00\x00')
        file.write(f"{author}/acc-".encode('utf-8'))
        for i in range(0, 23):
            file.write(b'\x00')
        file.close()
        
def generate_md5_from_str(_str: str) -> str:
    """Generates an MD5 hash from a string."""
    text_bytes = _str.encode('utf-8')
    hash_md5 = hashlib.md5(text_bytes)
    return hash_md5.hexdigest()

def current_time_str() -> str:
    """Returns the current time in a string format."""
    return time.strftime("%Y%m%d-%H%M%S")

def convert_image_to_jpg(path: str, img: Image, quality: int = 95) -> bool:
    """Converts the selected thumbnail to a JPEG image."""
    scene = bpy.context.scene
    config = scene.render.image_settings
    
    config.file_format = 'JPEG'
    config.quality = quality
    
    try:
        img.save_render(path + "/thumbnail1.jpg", scene=scene)
        return True
    except Exception as e:
        print(f"Error converting image: {str(e)}")
        return False
    
def create_folder(name: str) -> str:
    """Creates a folder using the hashed name from the object and current time in the export directory."""
    path = bpy.path.abspath(f"//{name.upper()}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def export_obj_as_glb(obj: Object, filepath: str, name: str) -> None:
    """Exports an object as a GLB file."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=filepath + f"/{name}.glb", use_selection=True, export_animations=False, export_draco_mesh_compression_enable=False, export_format='GLB')
    obj.select_set(False)
    
    
def update_path(self, context):
    """Updates the path to make it always absolute."""
    if self.inzoider_3d_crafts_path != '':
        self.inzoider_3d_crafts_path = bpy.path.abspath(self.inzoider_3d_crafts_path)

def change_visual_rotation_to_obj(obj: Object, apply: bool) -> None:
    """Applies or unapplies a 90-degree rotation to the Z axis visually and resets the rotation data."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.rotation_mode = 'XYZ'
    if apply:
        obj.rotation_euler.z = radians(90)
    else:
        obj.rotation_euler.z = radians(-90)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    obj.select_set(False)

def change_selection(self, context):
    selected_item = context.scene.obj_craft_list[context.scene.obj_craft_index]
    if selected_item:
        bpy.ops.object.select_all(action='DESELECT')
        selected_item.mesh.select_set(True)