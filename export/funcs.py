from bpy.types import Object, Image
import hashlib
import bpy

def get_obj_extents(obj: Object) -> tuple:
    """Gets proper extents of object to match inZOI scale."""
    return obj.dimensions * 50

def create_printed_file(author: str, file_path: str) -> None:
    with open(f"{file_path}/printed.bin", 'wb+') as file:
        file.write(b'\x01\x00\x00\x00\x25\x00\x00\x00')
        file.write(f"{author}/acc-".encode('utf-8'))
        for i in range(0, 23):
            file.write(b'\x00')
        file.close()
        
def generate_md5_from_str(_str: str) -> str:
    text_bytes = _str.encode('utf-8')
    hash_md5 = hashlib.md5(text_bytes)
    return hash_md5.hexdigest()


def convert_image_to_jpg(path: str, img: Image, quality: int = 95) -> bool:
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
    import os
    path = bpy.path.abspath(f"//{name}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path