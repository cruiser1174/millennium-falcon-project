from flask import Flask, redirect, request, session, url_for
from galaxy_structure import generate_galaxy, reveal_bounty_hunters, get_routes_data, open_json
from millenium_falcon_mainframe import calculate_path
from test_scan import get_all_json_files
import secrets

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
        del galaxy_data[galaxy_name]['routes_db']
    
    api_data['galaxies'] = galaxy_data
    api_data['scenarios'] = get_all_json_files(paths['scenarios'])
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
    falcon_data = open_json(falcon_path)
    starting_data = {
        'departure_planet': falcon_data['departure'],
        'destination_planet': falcon_data['arrival'],
        'fuel_capacity': falcon_data['autonomy'],
        'time_limit': data['scenario']['countdown'],
        'start_day': 0
    }

    a_galaxy_far_far_away = generate_galaxy(falcon_path)
    reveal_bounty_hunters(a_galaxy_far_far_away, data['scenario'])
    odds_array = calculate_path(a_galaxy_far_far_away, starting_data)
    print(odds_array)
    print(type(odds_array))
    #return {"odds": [1,2,3,4]}
    return odds_array

@galaxy_api.route('/get-routes-api')
def get_routes():
    #odds_array = request.args['odds_array']
    #odds_array = session['odds_array']
    #return odds_data
    #print(odds_data)
    return {'test': [1,2,3,4]}

if __name__ == '__main__':
    a = get_all_json_files(paths['galaxies'])
    print(a)