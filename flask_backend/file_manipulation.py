import json

# function converts and returns a json file into a python dictionary
def open_json(file_name: str) -> dict:
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data

# handy function for removing filename from a path
def remove_path_tail(path: str) -> str:
    split_path = path.split('\\')
    if len(split_path) > 1:
        return '\\'.join(split_path[:-1])+'\\'
    else:
        return ''