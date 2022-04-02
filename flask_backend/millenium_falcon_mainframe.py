from heapq import heappop, heappush
from universe import Galaxy
from math import inf
from galaxy_structure import open_json, generate_galaxy, reveal_bounty_hunters

"""
# extract starting, finishing planets and autonomy from falcon_data
starting_data = {
    'departure_planet': falcon_data['departure'],
    'destination_planet': falcon_data['arrival'],
    'fuel_capacity': falcon_data['autonomy'],
    'time_limit': empire_data['countdown']
}
"""

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



def updating_fn(return_data: dict, current_planet_data: dict, neighbor_planet_data: dict, planets_to_visit: list, galaxy: Galaxy):
    # set the current planet's hunter count, appending to the list of counts for all 
    # planets in this path
    return_data[current_planet_data['name']][1] = current_planet_data['hunter_count']

    neighbor_planet_data['hunter_count'] = current_planet_data['hunter_count']
    if are_bounty_hunters(galaxy, neighbor_planet_data['days'][-1], neighbor_planet_data['name']):
        neighbor_planet_data['hunter_count'] += 1

    # updat the neighbor's path data with: 
    # 1. day of arrival. 
    # 2. hunter counts on path. 
    # 3. path to the neighbor. 
    # 4. arrival fuel.
    print('\n')
    print('current planet: {} - days = {} - path = {}'.format(current_planet_data['name'], current_planet_data['arrival_days'], current_planet_data['path'] ))
    print('neighbor planet: {} - days = {} - path = {}'.format(neighbor_planet_data['name'], neighbor_planet_data['days'], neighbor_planet_data['path'] ))
    print('\n')
    #print('Planet: {}, old days: {}, new_days: {}'.format(neighbor_planet_data['name'], return_data[current_planet_data['name']][0], return_data[current_planet_data['name']][0] + [neighbor_planet_data['day']] ))
    return_data[neighbor_planet_data['name']] = [
        neighbor_planet_data['days'], 
        neighbor_planet_data['hunter_count'], 
        neighbor_planet_data['path'], 
        neighbor_planet_data['fuel']]
    
    # add the neighbor to the list of planets to visit
    heappush(
        planets_to_visit, 
        (
            neighbor_planet_data['hunter_count'],
            neighbor_planet_data['days'], 
            neighbor_planet_data['fuel'], 
            neighbor_planet_data['name'], 
            current_planet_data['name'],  
            neighbor_planet_data['path']))



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

    neighbor_arrival_data['day'] = neighbor_arrival_day_after_waiting
    current_planet_data['day'] = day_after_waiting

    return days_waiting

def stay_the_night(galaxy: Galaxy, current_planet_departure_data: dict, fuel_capacity: int):
    # increment the day
    current_planet_departure_data['day'] += 1
    # refuel
    current_planet_departure_data['fuel'] = fuel_capacity
    # check for bounty hunters in the morning
    if are_bounty_hunters(galaxy, current_planet_departure_data['day'], current_planet_departure_data['name']):
        current_planet_departure_data['hunter_count'] += 1


def calculate_path(galaxy: Galaxy, starting_data: dict) -> dict:
    time_limit = starting_data['time_limit']
    starting_planet_name = starting_data['departure_planet']
    finishing_planet_name = starting_data['destination_planet']
    fuel_capacity = starting_data['fuel_capacity']
    start_day = starting_data['start_day']

    #initialise path data dictionary to hold viable paths for falcon
    path_data = {}

    # fill return data for all planets initially with 
        # 1. infinite time to get there.
        # 2. a list with infinite days with bounty hunters. 
        # 3. a path list with the start planet in it. 
        # 4. the amount of fuel in the falcon when it arrived at the planet on the end of the path.
    for planet in galaxy.planets:
        path_data[planet] = [[start_day], inf, [starting_planet_name], 0]
    
    # manually set the return paths data for the starting planet
    path_data[starting_planet_name] = [[start_day], 0, [starting_planet_name], fuel_capacity]

    # initialise planets to visit minheap as a list of tuples, containing: 
    # 1. the number of hunters encountered to date 
    # 2. the time in days when arriving at the planet. 
    # 3. the current fuel capacity when arriving at the planet. 
    # 4. the name of the planet
    # 5. the name of the previous planet
    # 6. path to date
    planets_to_visit = [(0, [start_day], fuel_capacity, starting_planet_name, None, [starting_planet_name])]


    # when there are still planets to visit, and there is not a valid path to the 
    # final destination (when the number of bounty hunters encountered is infinity)
    while planets_to_visit:
        # extract data from planets to visit minheap, popping the tuple from the heap in the process
        arrival_hunter_count, arrival_days, arrival_fuel, current_planet_name, previous_planet_name, arrival_path = heappop(planets_to_visit)
        
        # get the current planet object from the galexy
        arrival_planet = galaxy.planets[current_planet_name]

        # create a copy of the current planet's neighbors, from which the previous planet can be deleted 
        # without altering the planet's object
        neighbors_minus_previous = arrival_planet.neighbors.copy()

        # if there was a previous planet, delete it from the copy (excludes start planet case)
        #if previous_planet_name:
         #   del neighbors_minus_previous[previous_planet_name]
        
        # loop through each neighbor, excluding previous planet
        for neighbor in neighbors_minus_previous:
            # set the current fuel, day, hunters and path to the arrival day at the current planet. These can be altered 
            # if for example the falcon must stay a night and refuel
            current_planet_departure_data = {
                'name': current_planet_name,
                'arrival_days': arrival_days,
                'day': arrival_days[-1],
                'fuel': arrival_fuel,
                'hunter_count': arrival_hunter_count,
                'path': arrival_path,
                'days_to_neighbor': neighbors_minus_previous[neighbor]
            }
            
            # If there are bounty hunters at the current planet then increase the hunter count
            #if are_bounty_hunters(galaxy, current_planet_departure_data['day'], current_planet_name):
            #    current_planet_departure_data['hunter_count'] += 1

            # If there is not enough fuel to get to the neighbor, then need to stay the night, increnmenting time and 
            # dealing with hunters
            if current_planet_departure_data['fuel'] < current_planet_departure_data['days_to_neighbor']:
                stay_the_night(galaxy, current_planet_departure_data, fuel_capacity)
            
            # set up neighbour arrival data the check whether to travel to the neighbour and
            neighbor_arrival_data = {
            'name': neighbor,
            'days': arrival_days + [current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor']],
            'day': current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor'],
            'fuel': current_planet_departure_data['fuel'] - current_planet_departure_data['days_to_neighbor'],
            'path': current_planet_departure_data['path'] + [neighbor]
            }

            # check whether can reach neighbor withing time limit
            if neighbor_arrival_data['day'] <= time_limit:
                # if less bounty hunters are encountered on this path to the neighbor than a previous checked 
                # path then make this the ideal path to that planet
                if current_planet_departure_data['hunter_count'] < path_data[neighbor][1]:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, galaxy)
                    
                # if the number of hunters encountered up to arrival at the neighbor is the same as 
                # before, then only update to the current path if the arrival fuel is greater than the 
                # past path. This will cover any case where the current path arrival allows the falcon to 
                # leave the neighbor planet instantly and potentially avoid an extra day hiding from hunters, 
                # while preventing the need to check for hunters at the neighbor or loop through all of the 
                # neighbor's neighbors to check if refuelling is needed
                elif current_planet_departure_data['hunter_count'] == path_data[neighbor][1] and neighbor_arrival_data['fuel'] > path_data[neighbor][3]:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, galaxy)
            
            days_waiting = calculate_wait_time(galaxy, current_planet_departure_data, neighbor_arrival_data, time_limit)

            if days_waiting and neighbor_arrival_data['day'] <= time_limit:
                #refuel while waiting
                current_planet_departure_data['fuel'] = fuel_capacity
                #updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit)
                recursive_start_data = {
                    'departure_planet': neighbor_arrival_data['name'],
                    'destination_planet': finishing_planet_name,
                    'fuel_capacity': neighbor_arrival_data['fuel'],
                    'time_limit': time_limit,
                    'start_day': neighbor_arrival_data['day']
                }
                recursive_return = calculate_path(galaxy, recursive_start_data)
                if recursive_return['odds'] > 0:
                    return {
                        'odds': (recursive_return['odds'] * calculate_prob(current_planet_departure_data['hunter_count']))/100,
                        'days': path_data[current_planet_name][0] + recursive_return['days'],
                        'path': current_planet_departure_data['path'] + recursive_return['path']
                    }

    
    destination_path_data = path_data[finishing_planet_name]
    odd_of_success = calculate_prob(destination_path_data[1])
    
    return_data = {
        'odds': odd_of_success,
        'days': destination_path_data[0],
        'path': destination_path_data[2]
    }

    return return_data

if __name__ == '__main__':
    falcon_path = 'Provided_Examples\\example4\\millennium-falcon.json'
    empire_path = 'Provided_Examples\\example4\\empire.json'
    falcon_data = open_json(falcon_path)
    empire_data = open_json(empire_path)
    a_galaxy_far_far_away = generate_galaxy(falcon_path)
    reveal_bounty_hunters(a_galaxy_far_far_away, empire_data)

    # extract starting, finishing planets and autonomy from falcon_data
    starting_data = {
        'departure_planet': falcon_data['departure'],
        'destination_planet': falcon_data['arrival'],
        'fuel_capacity': falcon_data['autonomy'],
        'time_limit': empire_data['countdown'],
        'start_day': 0
    }

    optimal_path_data = calculate_path(a_galaxy_far_far_away, starting_data)

    print(optimal_path_data)