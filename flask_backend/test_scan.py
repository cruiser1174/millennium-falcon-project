import os
from galaxy_structure import open_json

paths = {
    'galaxies': '\galaxies',
    'scenarios': 'flask_backend\scenarios'
}

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

    




            
