import json, os

# function converts a json file into a python dictionary and returns it
def open_json(file_name: str) -> dict:
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data

# handy function for removing filename from a path
def remove_path_tail(path: str) -> str:
    # split path by backslashes
    split_path = path.split('\\')

    # if there is more than one slash then return 
    # everything before (the root)
    if len(split_path) > 1:
        return '\\'.join(split_path[:-1])+'\\'
    else:
        return ''

# removes file extension such as '.json' from a path - allowing easier editing of 
# file names when uploading files, preventing overwriting of non-unique file names
def clip_file_name(file_name: str) -> str:
    return '.'.join(file_name.split('.')[:-1])

# For a given path to a directory, retrieves data from every json file in that 
# directory and returns it in a single python dictionary with keys of the names of 
# the json files
def get_all_json_files(directory_path: str) -> dict:
    data = {}
    for file_path in os.scandir(directory_path):
        if file_path.name.endswith('.json'):
            filename = clip_file_name(file_path.name)
            filedata = open_json(file_path)
            data[filename] = filedata
    return data

# function to process the scenario json (empire.json) files from a certain directory 
# into the correct format for feeding through to the frontend for rendering. Returns 
# a dictionary with the scenario filenames as keys, with an embedded dictionary with 
# the scenario time limit and a dictionary of planets with the days on which they have 
# bounty hunters in string format (only needs to be string as it will just be displayed 
# on the frontend, no calculations are necessary)
def get_react_scenario_data(directory_path: str) -> dict:
    return_data = {}
    scenarios_data = get_all_json_files(directory_path)

    for scenario in scenarios_data:
        return_data[scenario] = {'countdown': scenarios_data[scenario]['countdown']}
        bounty_data = scenarios_data[scenario]['bounty_hunters']
        planets = {}
        for entry in bounty_data:
            if entry['planet'] not in planets:
                planets[entry['planet']] = str(entry['day'])
            else:
                planets[entry['planet']] += ', {}'.format(entry['day'])
        return_data[scenario]['planets'] = planets
    
    return return_data