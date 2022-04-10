from heapq import heappop, heappush
from universe import Galaxy
from math import inf
from file_manipulation import open_json
from galaxy_structure import generate_galaxy, reveal_bounty_hunters
import copy

def calculate_prob(n: int) -> float:
    prob = 0
    if n == inf:
        return 0
    for i in range(1, n+1):
        prob += 9**(i-1) / 10**i
    return 100*(1 - prob)



# checks if there will be bounty hunters at a particular planet on a particular day
def are_bounty_hunters(galaxy: Galaxy, day: int, planet_name: str) -> bool:
    if day in galaxy.planets[planet_name].bounty_hunter_days:
        return True
    else:
        return False



def updating_fn(return_data: dict, current_planet_data: dict, neighbor_planet_data: dict, planets_to_visit: list, destination_planet: str):
    # set the current planet's hunter count, appending to the list of counts for all 
    # planets in this path
    return_data[current_planet_data['name']]['hunter_count'] = current_planet_data['hunter_count']

    current_planet_data['path_data'][-1]['departure_day'] = current_planet_data['day']
    current_planet_data['path_data'][-1]['refueled'] = current_planet_data['refueled']
    current_planet_data['path_data'][-1]['waited_for_hunters'] = current_planet_data['waited_for_hunters']
    current_planet_data['path_data'][-1]['hunter_count'] = current_planet_data['hunters']

    return_data[current_planet_data['name']]['path_data'] = current_planet_data['path_data']
    
    neighbor_planet_data['path_data'] = current_planet_data['path_data'] + [{
        'planet': neighbor_planet_data['name'], 
        'arrival_day':  neighbor_planet_data['arrival_days'][-1], 
        'hunter_count': neighbor_planet_data['hunters']}]

    # updat the neighbor's path data with: 
    # 1. day of arrival. 
    # 2. hunter counts on path. 
    # 3. path to the neighbor. 
    # 4. arrival fuel.
    return_data[neighbor_planet_data['name']] = {
        'arrival_days': neighbor_planet_data['arrival_days'], 
        'hunter_count': neighbor_planet_data['hunter_count'], 
        'path_data': neighbor_planet_data['path_data'], 
        'fuel_level': neighbor_planet_data['fuel']}
    
    # add the neighbor to the list of planets to visit if it is not the 
    # destination planet (there's no need to travel on from the destination planet)
    if neighbor_planet_data['name'] != destination_planet:
        heappush(
            planets_to_visit, 
            (
                neighbor_planet_data['hunter_count'],
                neighbor_planet_data['arrival_days'], 
                neighbor_planet_data['fuel'], 
                neighbor_planet_data['name'], 
                neighbor_planet_data['path_data']))



def calculate_wait_time(galaxy: Galaxy, current_planet_data: dict, neighbor_arrival_data: dict, time_limit: int) -> int:
    day_after_waiting = current_planet_data['day']
    neighbor_arrival_day_after_waiting = neighbor_arrival_data['day']
    days_waiting = 0

    while are_bounty_hunters(galaxy, neighbor_arrival_day_after_waiting, neighbor_arrival_data['name']):
        if are_bounty_hunters(galaxy, day_after_waiting, current_planet_data['name']) or neighbor_arrival_day_after_waiting > time_limit:
            # don't wait at all
            return 0
        days_waiting += 1
        day_after_waiting += 1
        neighbor_arrival_day_after_waiting += 1

    return days_waiting

def stay_the_night(galaxy: Galaxy, current_planet_departure_data: dict, fuel_capacity: int):
    # increment the day
    current_planet_departure_data['day'] += 1
    # refuel
    if current_planet_departure_data['fuel'] < fuel_capacity:
        current_planet_departure_data['fuel'] = fuel_capacity
        current_planet_departure_data['refueled'] = True
    # check for bounty hunters in the morning
    if are_bounty_hunters(galaxy, current_planet_departure_data['day'], current_planet_departure_data['name']):
        current_planet_departure_data['hunter_count'] += 1
        current_planet_departure_data['hunters'] += 1

def revise_neighbor_data(neighbor_data: dict, days_waiting: int):
    neighbor_data['hunter_count'] -= 1
    neighbor_data['hunters'] -= 1
    neighbor_arrival_day_after_waiting = neighbor_data['day'] + days_waiting
    neighbor_data['day'] = neighbor_arrival_day_after_waiting
    neighbor_data['arrival_days'] = neighbor_data['arrival_days'][:-1] + [neighbor_arrival_day_after_waiting]
                        
def revise_current_data(current_data: dict, days_waiting: int):
    departure_day_after_waiting = current_data['day'] + days_waiting
    current_data['day'] = departure_day_after_waiting
    current_data['waited_for_hunters'] = True
    current_data['path_data'][-1]['departure_day'] = current_data['day']
    current_data['path_data'][-1]['waited_for_hunters'] = current_data['waited_for_hunters']
    current_data['path_data'][-1]['hunter_count'] = current_data['hunters']

def refuel(planet_data: dict, fuel_capacity: int):
    if planet_data['fuel'] < fuel_capacity:
        planet_data['fuel'] = fuel_capacity
        planet_data['refueled'] = True
    
    planet_data['path_data'][-1]['refueled'] = planet_data['refueled']

def push_to_heap(heap: list, planet_data):
    heappush(
        heap, 
        (
            planet_data['hunter_count'],
            planet_data['arrival_days'], 
            planet_data['fuel'], 
            planet_data['name'], 
            planet_data['path_data']))

def calculate_path(galaxy: Galaxy, starting_data: dict) -> dict:
    #initialise path data dictionary to hold viable paths for falcon
    path_data = {}

    # fill path data for all planets initially with:
    # 1. array of arrival days at previous planets on path, starting with jusy day 0 at first planet
    # 2. having spent an infinite number of days with bounty hunters (worst case scenario) 
    # 3. a path list of dictionaries, where each dictionary contains a planet on the path to the planet 
    #       in question, along with key details about the path - arrival days, departure days, time spent 
    #       with hunters, refuelling and waiting for bounty hunters
    # 4. the amount of fuel in the falcon when it arrived at the planet in question
    for planet in galaxy.planets:
        path_data[planet] = {
            'arrival_days': [0], 
            'hunter_count': inf, 
            'path_data': [{'planet': starting_data['departure_planet'], 'arrival_day': 0, 'hunter_count': 0}], 
            'fuel_level': 0}
    
    # manually set the return path data for the starting planet
    path_data[starting_data['departure_planet']] = {
            'arrival_days': [0], 
            'hunter_count': 0, 
            'path_data': [{'planet': starting_data['departure_planet'], 'arrival_day': 0, 'hunter_count': 0}], 
            'fuel_level': starting_data['fuel_capacity']}

    # initialise planets to visit minheap as a list of tuples, containing: 
    # 1. the number of hunters encountered to date 
    # 2. a list of arrival days at the planets along the path
    # 3. the current fuel capacity when arriving at the planet. 
    # 4. the name of the planet arrived at
    # 6. path to date
    planets_to_visit = [(
        0, 
        [0], 
        starting_data['fuel_capacity'], 
        starting_data['departure_planet'], 
        [{'planet': starting_data['departure_planet'],'arrival_day': 0, 'hunter_count': 0}])]


    # when there are still planets to visit - pop the planet with smallest hunter count of the heap of 
    # planets to visit and then check the path of travelling to that planet's neighbors
    while planets_to_visit:
        # extract data from planets to visit minheap, popping the tuple from the heap in the process
        arrival_hunter_count, arrival_days, arrival_fuel, current_planet_name, arrival_path = heappop(planets_to_visit)
        # get the current planet object from the galexy
        arrival_planet = galaxy.planets[current_planet_name]
        
        # loop through each neighbor, excluding previous planet
        for neighbor in arrival_planet.neighbors:
            # Set dictionary of current planet details. These can be altered 
            # if for example the falcon must stay a night and refuel
            current_planet_departure_data = {
                'name': current_planet_name,
                'arrival_days': arrival_days,
                'day': arrival_days[-1],
                'fuel': arrival_fuel,
                'hunter_count': arrival_hunter_count,
                'path_data': arrival_path,
                'days_to_neighbor': arrival_planet.neighbors[neighbor],
                'refueled': False,
                'waited_for_hunters': False,
                'hunters': arrival_path[-1]['hunter_count']
            }

            # If there is not enough fuel to get to the neighbor, then need to stay the night, increnmenting time and 
            # dealing with hunters
            if current_planet_departure_data['fuel'] < current_planet_departure_data['days_to_neighbor']:
                stay_the_night(galaxy, current_planet_departure_data, starting_data['fuel_capacity'])
            
            # set up neighbour arrival data the check whether to travel to the neighbour or not
            neighbor_arrival_data = {
            'name': neighbor,
            'arrival_days': arrival_days + [current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor']],
            'day': current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor'],
            'fuel': current_planet_departure_data['fuel'] - current_planet_departure_data['days_to_neighbor'],
            'hunter_count': current_planet_departure_data['hunter_count'],
            'hunters': 0
            }
            print("Looking to travel from {} to {}".format(current_planet_name, neighbor))

            # check whether can reach neighbor withing time limit, if so, attempt to make the journey
            if neighbor_arrival_data['day'] <= starting_data['time_limit']:
                # if there are bounty hunters at the neighbor planet on the arrival day, add one to the 
                # neighbor's hunter count, and the total path hunter count
                if are_bounty_hunters(galaxy, neighbor_arrival_data['day'], neighbor):
                    neighbor_arrival_data['hunter_count'] += 1
                    neighbor_arrival_data['hunters'] += 1
                    
                # if less bounty hunters are encountered on this path to the neighbor than the previous best 
                # path calculated to the neighbor then make this the ideal path to that neighboring planet, 
                # adding the neighbor to the heap of planets to visit as long as it is not the destination planet
                if neighbor_arrival_data['hunter_count'] < path_data[neighbor]['hunter_count']:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, starting_data['destination_planet'])
                    print("SUCCESSFUL TRAVEL")
                    
                # if the number of hunters encountered up to arrival at the neighbor is the same as 
                # before, then only update to the current path if the arrival fuel is greater than the 
                # past path. This will cover any case where the current path arrival allows the falcon to 
                # leave the neighbor planet instantly and potentially avoid an extra day hiding from hunters, 
                # while preventing the need to check for hunters at the neighbor or loop through all of the 
                # neighbor's neighbors to check if refuelling is needed
                elif neighbor_arrival_data['hunter_count'] == path_data[neighbor]['hunter_count'] and neighbor_arrival_data['fuel'] > path_data[neighbor]['fuel_level']:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, starting_data['destination_planet'])
                    print("SUCCESSFUL TRAVEL")

                # if there are bounty hunters at the neighbor planet, check to see if the falcon can wait for them to leave
                if are_bounty_hunters(galaxy, neighbor_arrival_data['day'], neighbor_arrival_data['name']):
                    
                    # days waiting is the return of a function that checks if the falcon can wait for a number of days and still arrive 
                    # at the neighbor planet before the time limit and while there are no hunters there or at the current planet, otherwise returning 0
                    days_waiting = calculate_wait_time(galaxy, current_planet_departure_data, neighbor_arrival_data, starting_data['time_limit'])
                    if days_waiting:
                        # create deep copies of current planet and neighbor planet data so that it can be edited to add to the heap of planets to visit, 
                        # without affecting the heap addituion from not waiting. This is impotant because if it turns out that down the line the falcon 
                        # runs out of time on the path after waiting, then we still need to path from not waiting
                        current_planet_waiting_data = copy.deepcopy(current_planet_departure_data)
                        neighbor_waiting_data = copy.deepcopy(neighbor_arrival_data)

                        # revise current planet and neighbor data to account for days waiting
                        revise_current_data(current_planet_waiting_data, days_waiting)
                        revise_neighbor_data(neighbor_waiting_data, days_waiting)

                        # refuel while waiting
                        refuel(current_planet_waiting_data, starting_data['fuel_capacity'])
                        
                        # update neighbor arriving fuel and path data
                        neighbor_waiting_data['fuel'] = current_planet_waiting_data['fuel'] - current_planet_waiting_data['days_to_neighbor']
                        neighbor_waiting_data['path_data'] = current_planet_waiting_data['path_data'] + [{
                            'planet': neighbor_waiting_data['name'], 
                            'arrival_day': neighbor_waiting_data['day'], 
                            'hunter_count': neighbor_waiting_data['hunters']}]

                        # add neighbor to planets to visit if it is not the destination planet                        
                        if neighbor_waiting_data['name'] != starting_data['destination_planet']:
                            push_to_heap(planets_to_visit, neighbor_waiting_data)


    # get the optimal path data (least days with bounty hunters) for destination 
    # planet and calculate the odds of success based on that number of days with hunters
    destination_path_data = path_data[starting_data['destination_planet']]
    odd_of_success = calculate_prob(destination_path_data['hunter_count'])
    
    return_data = {
        'odds': odd_of_success,
        'path_data': destination_path_data['path_data']
    }
    
    return return_data

if __name__ == '__main__':
    falcon_path = 'flask_backend\galaxies\millennium-falcon-1.json'
    empire_path = 'flask_backend\scenarios\empire-1.json'
    falcon_data = open_json(falcon_path)
    empire_data = open_json(empire_path)
    a_galaxy_far_far_away = generate_galaxy(falcon_path)
    reveal_bounty_hunters(a_galaxy_far_far_away, empire_data)

    # extract starting, finishing planets and autonomy from falcon_data
    starting_data = {
        'departure_planet': falcon_data['departure'],
        'destination_planet': falcon_data['arrival'],
        'fuel_capacity': falcon_data['autonomy'],
        'time_limit': empire_data['countdown']
    }

    optimal_path_data = calculate_path(a_galaxy_far_far_away, starting_data)

    print(optimal_path_data)