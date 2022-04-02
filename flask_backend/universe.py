
# Create Planet class, objects of which will make up the Galaxy
class Planet:
    def __init__(self, name: str):
        self.planet_name = name
        self.neighbors = {}
        self.bounty_hunter_days = []
    
    # method to add a neighbour, where neighbor is another Planet object
    # and length is the time in days it takes to travel between the neighbors
    def add_neighbour(self, neighbour_name: str, length: int):
        self.neighbors[neighbour_name] = length
    
    # returning a list of all the neighbors of a given planet
    def get_neighbours(self) -> list:
        return list(self.neighbors.keys())
    
    # add bounty hunter day - sets a value of true in the has_bounty_hunters
    # dict, where the key i the day
    def add_bounty_hunters(self, day: int):
        self.bounty_hunter_days.append(day)

# Create Galaxy class - effectively a graph that will be composed of the
# planets that are defined in routes_db supplied from millenium-falcon.json
class Galaxy:
    def __init__(self):
        self.planets = {}
    
    def add_planet(self, planet: Planet):
        self.planets[planet.planet_name] = planet
    
    def add_route(self, start_planet: Planet, end_planet: Planet, length: int):
        self.planets[start_planet.planet_name].add_neighbour(
            end_planet.planet_name, 
            length)

        self.planets[end_planet.planet_name].add_neighbour(
            start_planet.planet_name, 
            length)
    
    # handy function that displays the structure and contents of the galaxy 
    # to the console
    def display(self):
        for planet_name in self.planets:
            neighbors = self.planets[planet_name].neighbors
            bounty_days = self.planets[planet_name].bounty_hunter_days
            print(planet_name)
            print('Neighbors are:')
            for neighbor in neighbors:
                print('{} - {} days away'.format(
                    neighbor, 
                    neighbors[neighbor]))
            
            if bounty_days:
                print('Will have bounty hunters on:')
                for day in bounty_days:
                    print('Day {}'.format(day))
            else:
                print('Safe from bounty hunters')
            print('\n')
