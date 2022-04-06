from flask import Flask, redirect, request, session, url_for
from galaxy_structure import generate_galaxy, reveal_bounty_hunters, get_routes_data, open_json
from millenium_falcon_mainframe import calculate_path
from test_scan import get_all_json_files, clip_file_name, get_react_scenario_data
import secrets
import os

galaxy_api = Flask(__name__)
secret = secrets.token_hex(16)
galaxy_api.config['SECRET_KEY'] = secret
# define relative paths to galaxies and scenarios folders which hold the 
# millennium falcon and empire json files
paths = {
    'galaxies': 'galaxies',
    'scenarios': 'scenarios'
}

odds_data = {}

# initialisation api which feeds the existing galaxies and scenarios to the 
# react frontend for users to choose from. Will take all json files from the path 
# directories and return them, so make sure that only the correct json files are kept 
# in these directories
@galaxy_api.route('/galaxy-api')
def send_galaxy():
    api_data = {}
    galaxy_data = get_all_json_files(paths['galaxies'])
    for galaxy_name in galaxy_data:
        galaxy = generate_galaxy('{}\\{}.json'.format(paths['galaxies'], galaxy_name))
        galaxy_data[galaxy_name]['planets'] = list(galaxy.planets.keys())
        galaxy_data[galaxy_name]['neighbors'] = {}
        for planet in galaxy.planets:
            galaxy_data[galaxy_name]['neighbors'][planet] = galaxy.planets[planet].neighbors
        del galaxy_data[galaxy_name]['routes_db']
    
    api_data['galaxies'] = galaxy_data
    api_data['scenarios'] = get_react_scenario_data(paths['scenarios'])
    print(api_data['galaxies'])
    print(api_data['scenarios'])
    return api_data

@galaxy_api.route('/send-bounty-hunters-api', methods = ['GET', 'POST'])
def get_bounty_hunters():
    if request.method == 'POST':
        bounty_hunter_data = request.get_json()
        print(bounty_hunter_data)
        return bounty_hunter_data

@galaxy_api.route('/calculate-odds-api', methods = ['GET', 'POST'])
def calculate_odds():
    odds_array = []
    data = request.get_json()
    falcon_path = 'galaxies\\{}.json'.format(data['galaxy'])
    scenario_path = 'scenarios\\{}.json'.format(data['scenario'])
    falcon_data = open_json(falcon_path)
    scenario_data = open_json(scenario_path)
    starting_data = {
        'departure_planet': falcon_data['departure'],
        'destination_planet': falcon_data['arrival'],
        'fuel_capacity': falcon_data['autonomy'],
        'time_limit': scenario_data['countdown'],
        'start_day': 0
    }

    a_galaxy_far_far_away = generate_galaxy(falcon_path)
    reveal_bounty_hunters(a_galaxy_far_far_away, scenario_data)
    odds_array = calculate_path(a_galaxy_far_far_away, starting_data)
    print(odds_array)
    return odds_array

@galaxy_api.route('/get-routes-api')
def get_routes():
    #odds_array = request.args['odds_array']
    #odds_array = session['odds_array']
    #return odds_data
    #print(odds_data)
    return {'test': [1,2,3,4]}

@galaxy_api.route('/upload-scenario-api', methods = ['GET', 'POST'])
def upload_scenario():
    api_data ={}

    file = request.files['file']
    filename = file.filename
    original_filename = clip_file_name(filename)
    file_path = os.path.join('scenarios', filename)

    count = 2
    while os.path.isfile(file_path):
        filename = '{}-{}.json'.format(original_filename, count)
        file_path = os.path.join('scenarios', filename)
        count += 1
    
    file.save(file_path)
    file_data = open_json(file_path)
    file_keys = list(file_data.keys())
    if file_keys != ['countdown', 'bounty_hunters'] and file_keys != ['bounty_hunters', 'countdown']:
        os.remove(file_path)
        print("File data invalid - incorrect keys - file keys are {}, ensure they are ['countdown', 'bounty_hunters']".format(file_keys))
        api_data['alert'] = "File data invalid - incorrect keys - file keys are {}, ensure they are ['countdown', 'bounty_hunters']".format(file_keys)
        return api_data
    
    
    api_data['scenarios'] = get_react_scenario_data(paths['scenarios'])
    
    api_data['alert'] = "Upload successful - you can now select this scenario as '{}' from the dropdown menu".format(clip_file_name(filename))

    return api_data

if __name__ == '__main__':
    a = get_all_json_files(paths['galaxies'])
    print(a)