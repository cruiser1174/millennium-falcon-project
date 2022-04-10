import sqlite3
from universe import Galaxy, Planet
from file_manipulation import open_json, remove_path_tail

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

# given path to galaxy (millennium falcon) json file, generates a complete galaxy object 
# without and bounty hunters
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


