from bpy.types import Object

def get_obj_extents(obj: Object):
    """Gets proper extents of object to match inZOI scale."""
    return obj.dimensions * 50

def create_printed_file(author: str, file_path: str):
    with open(f"{file_path}/printed.bin", 'wb+') as file:
        file.write(b'\x01\x00\x00\x00\x25\x00\x00\x00')
        file.write(f"{author}/acc-".encode('utf-8'))
        for i in range(0, 23):
            file.write(b'\x00')
        file.close()