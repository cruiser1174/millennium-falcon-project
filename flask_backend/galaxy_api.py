from flask import Flask, request
from galaxy_structure import generate_galaxy, reveal_bounty_hunters, open_json
from millenium_falcon_mainframe import calculate_path
from test_scan import get_all_json_files, clip_file_name, get_react_scenario_data
import os

galaxy_api = Flask(__name__)

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
    # get all of the galaxies (millennium falcon files) and turn into python dicts 
    galaxy_data = get_all_json_files(paths['galaxies'])

    # generate a galaxy objexct for each galaxy file then format data so that the api 
    # return-data will be a json where for each galaxy, there is a list of planets, and 
    # a list of neighbors for each planet 
    for galaxy_name in galaxy_data:
        galaxy = generate_galaxy('{}\\{}.json'.format(paths['galaxies'], galaxy_name))
        galaxy_data[galaxy_name]['planets'] = list(galaxy.planets.keys())
        galaxy_data[galaxy_name]['neighbors'] = {}
        for planet in galaxy.planets:
            galaxy_data[galaxy_name]['neighbors'][planet] = galaxy.planets[planet].neighbors
        del galaxy_data[galaxy_name]['routes_db']
    
    api_data['galaxies'] = galaxy_data

    # get all of the scenarios (empire json files) and save intop python dicts which are 
    # added to the api return data
    api_data['scenarios'] = get_react_scenario_data(paths['scenarios'])
    return api_data

# api that receives a selected galaxy and scenario name, retrieves the relevant data from 
# the backend, calculates the optimal path/odds and then returns it on the endpoint to be 
# rendered in the front end
@galaxy_api.route('/calculate-odds-api', methods = ['GET', 'POST'])
def calculate_odds():
    data = request.get_json()
    # get the file paths based on scenario names
    falcon_path = 'galaxies\\{}.json'.format(data['galaxy'])
    scenario_path = 'scenarios\\{}.json'.format(data['scenario'])
    # retrieve data from json files
    falcon_data = open_json(falcon_path)
    scenario_data = open_json(scenario_path)

    # define starting data which is an inpur for the calculate_path function which retrieves 
    # the odds of the optimal path
    starting_data = {
        'departure_planet': falcon_data['departure'],
        'destination_planet': falcon_data['arrival'],
        'fuel_capacity': falcon_data['autonomy'],
        'time_limit': scenario_data['countdown'],
        'start_day': 0
    }

    # generate the galaxy for the scenario
    a_galaxy_far_far_away = generate_galaxy(falcon_path)
    # populate the galaxy with its bounty hunters
    reveal_bounty_hunters(a_galaxy_far_far_away, scenario_data)

    # calculate and return the optimal path
    odds_path = calculate_path(a_galaxy_far_far_away, starting_data)
    return odds_path

# api which accepts an uploaded json file, checkes if it has the correct format and adds it 
# to the scenarios folder
@galaxy_api.route('/upload-scenario-api', methods = ['GET', 'POST'])
def upload_scenario():
    api_data ={}
    print("here")

    # get the uploaded file
    file = request.files['file']
    filename = file.filename

    # clip the end off the file, keeping just the name, and then create a path to the 
    # scenarios folder
    original_filename = clip_file_name(filename)
    file_path = os.path.join('scenarios', filename)

    # while there is a scenario with the same name in the scenarios folder, add an 
    # incremented number to the end of the new file path until it is a unique path, 
    # preventing overwriting of existing scenarios
    count = 2
    while os.path.isfile(file_path):
        filename = '{}-{}.json'.format(original_filename, count)
        file_path = os.path.join('scenarios', filename)
        count += 1
    
    # save the new file and open it, retrieving the data as a python dict
    file.save(file_path)
    file_data = open_json(file_path)

    # check that the keys are the values expected for the scenario, if not, then 
    # delete the uploaded file from the scenarios folder and return an alert to the 
    # frontend to instruct the user to make sure the uploaded file has the correct format
    file_keys = list(file_data.keys())
    if file_keys != ['countdown', 'bounty_hunters'] and \
        file_keys != ['bounty_hunters', 'countdown']:
        os.remove(file_path)
        api_data['alert'] = "File data invalid - incorrect keys - file keys are {}, \
            ensure they are ['countdown', 'bounty_hunters']".format(file_keys)
        return api_data
    
    # the format is correct, retrieve the new collection of scenarios and return it to 
    # the frontend for rendering. Return an alert with the filename so that the user knows 
    # if the scenario name was changed from what was uploaded
    api_data['scenarios'] = get_react_scenario_data(paths['scenarios'])
    api_data['alert'] = "Upload successful - you can now select this scenario as '{}' from the dropdown menu".format(clip_file_name(filename))
    print(api_data)
    return api_data

if __name__ == '__main__':
    a = get_all_json_files(paths['galaxies'])
    print(a)