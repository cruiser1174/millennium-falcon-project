import os
from galaxy_structure import open_json

def clip_file_name(file_name: str) -> str:
    return '.'.join(file_name.split('.')[0:-1])

def get_all_json_files(directory_path: str) -> dict:
    data = {}
    for file_path in os.scandir(directory_path):
        if file_path.name.endswith('.json'):
            filename = clip_file_name(file_path.name)
            filedata = open_json(file_path)
            data[filename] = filedata
    return data

#print(get_all_json_files('flask_backend\scenarios'))




            
