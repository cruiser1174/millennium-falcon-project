from flask import Flask, request
from galaxy_structure import generate_galaxy
from test_scan import get_all_json_files

galaxy_api = Flask(__name__)

# define relative paths to galaxies and scenarios folders which hold the 
# millennium falcon and empire json files
paths = {
    'galaxies': 'galaxies',
    'scenarios': 'scenarios'
}

# initialisation api which feeds the existing galaxies and scenarios to the 
# react frontend for users to choose from. Will take all json files from the path 
# directories and return them, so make sure that only the correct json files are kept 
# in these directories
@galaxy_api.route('/galaxy-api')
def send_galaxy():
    api_data = {}
    #galaxy_data = get_all_json_files(paths['galaxies'])
    #for galaxy_name in galaxy_data:
    #    galaxy = generate_galaxy('{}\\{}.json'.format(paths['galaxies'], galaxy_name))
    #    galaxy_data[galaxy_name]['planets'] = galaxy.planets
    #    del galaxy_data['routes_db']
    
    #api_data['galaxies'] = galaxy_data
    api_data['scenarios'] = get_all_json_files(paths['scenarios'])
    return api_data

@galaxy_api.route('/send-bounty-hunters-api', methods = ['GET', 'POST'])
def get_bounty_hunters():
    if request.method == 'POST':
        bounty_hunter_data = request.get_json()
        print(bounty_hunter_data)
        return bounty_hunter_data

@galaxy_api.route('/get-routes-api')
def get_routes():
    routes = {}
    return routes

if __name__ == '__main__':
    a = get_all_json_files(paths['galaxies'])
    print(a)