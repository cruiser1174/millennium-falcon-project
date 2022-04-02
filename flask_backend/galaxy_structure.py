import json
import sqlite3
from universe import Galaxy, Planet

#example_num = 4
#example_data_path = 'Provided_Examples\example{}'.format(example_num)

# function converts and returns a json file into a python dictionary
def open_json(file_name: str) -> dict:
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data

# given list of routes in the galaxy, initialises the planets
def populate_galaxy(galaxy: Galaxy, routes: list):
    # loop through each route
    for route in routes:
        # the first two indices are the planet names
        route_planets = list(route[:2])
        # for each of the 2 planet names, check if they are already in the galaxy
        for planet_name in route_planets:
            if planet_name not in galaxy.planets:
                #if the planets are not in the galaxy yet, add them to it
                planet = Planet(planet_name)
                galaxy.add_planet(planet)
        
        # add the route length between the two planets
        galaxy.add_route(
            galaxy.planets[route_planets[0]], 
            galaxy.planets[route_planets[1]], 
            route[2])


#get data from millenium-falcon.json
#falcon_data = open_json('{}\millennium-falcon.json'.format(example_data_path))
#empire_data = open_json('{}\empire.json'.format(example_data_path))
#bounty_hunter_locations = empire_data['bounty_hunters']

#falcon_autonomy = falcon_data['autonomy']
#departure_planet_name = falcon_data['departure']
#arrival_planet_name = falcon_data['arrival']

#open a connection to routes database
#db_connection = sqlite3.connect('{}\{}'.format(
 #   example_data_path, 
  #  falcon_data['routes_db']))

#db_cursor = db_connection.cursor()

# get table name from db, assuming required table is first table in db
#db_table_name = db_cursor.execute(
   # 'SELECT name from sqlite_master where type = "table"').fetchone()[0]

def remove_path_tail(path: str) -> str:
    split_path = path.split('\\')
    if len(split_path) > 1:
        return '\\'.join(split_path[:-1])+'\\'
    else:
        return ''

# Grabs all routes from the database, storing them in a list
#routes_data = db_cursor.execute('SELECT * FROM {}'.format(db_table_name)).fetchall()
def get_routes_data(falcon_path: str) -> list:
    #open a connection to routes database
    falcon_data = open_json(falcon_path)
    path_root = remove_path_tail(falcon_path) 
    db_connection = sqlite3.connect('{}{}'.format(path_root, falcon_data['routes_db']))
    db_cursor = db_connection.cursor()
    # get table name from db, assuming required table is first table in db
    db_table_name = db_cursor.execute('SELECT name from sqlite_master where type = "table"').fetchone()[0]
    # Grabs all routes from the database, storing them in a list
    routes_data = db_cursor.execute('SELECT * FROM {}'.format(db_table_name)).fetchall()
    return routes_data

def generate_galaxy(falcon_path: str) -> Galaxy:
    galaxy = Galaxy()
    routes_data = get_routes_data(falcon_path)
    populate_galaxy(galaxy, routes_data)
    return galaxy

# shows which planets have bounty hunters on which days. Does this by adding an entry
# into a planet's .has_bounty_hunters dict
def reveal_bounty_hunters(galaxy: Galaxy, empire_data: dict):
    bounty_hunter_data = empire_data['bounty_hunters']
    for record in bounty_hunter_data:
        galaxy.planets[record['planet']].add_bounty_hunters(record['day'])
    
#falcon_path = '{}\millennium-falcon.json'.format(example_data_path)
#empire_path = '{}\empire.json'.format(example_data_path)

#a_galaxy_far_far_away = generate_galaxy(falcon_path)

#populate_galaxy(a_galaxy_far_far_away, routes_data)
#reveal_bounty_hunters(a_galaxy_far_far_away, empire_path)

#a_galaxy_far_far_away.display()

