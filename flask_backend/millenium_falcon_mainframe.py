from heapq import heappop, heappush
from universe import Galaxy
from math import inf
from galaxy_structure import open_json, generate_galaxy, reveal_bounty_hunters
import copy

"""
NEED TO STOP ADDING PLANETS TO VISIT WHEN CUIRRENT PLANET IS DESTINATION PLANETY
"""

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
    return_data[current_planet_data['name']]['hunter_count'] = current_planet_data['hunter_count']

    current_planet_data['path_data'][-1]['departure_day'] = current_planet_data['day']
    current_planet_data['path_data'][-1]['refueled'] = current_planet_data['refueled']
    current_planet_data['path_data'][-1]['waited_for_hunters'] = current_planet_data['waited_for_hunters']
    current_planet_data['path_data'][-1]['hunter_count'] = current_planet_data['hunters']

    #print('\n')
    return_data[current_planet_data['name']]['path_data'] = current_planet_data['path_data']
    

    neighbor_planet_data['path_data'] = current_planet_data['path_data'] + [{'planet': neighbor_planet_data['name'], 'arrival_day':  neighbor_planet_data['arrival_days'][-1], 'hunter_count': neighbor_planet_data['hunters']}]
    
    
    #neighbor_planet_data['hunter_count'] = current_planet_data['hunter_count']
    #if are_bounty_hunters(galaxy, neighbor_planet_data['arrival_days'][-1], neighbor_planet_data['name']):
    #    neighbor_planet_data['hunter_count'] += 1

    # updat the neighbor's path data with: 
    # 1. day of arrival. 
    # 2. hunter counts on path. 
    # 3. path to the neighbor. 
    # 4. arrival fuel.
    #print('\n')
    #print('current planet: {} - days = {} - path = {}'.format(current_planet_data['name'], current_planet_data['arrival_days'], current_planet_data['path_data'] ))
    #print('neighbor planet: {} - days = {} - path = {}'.format(neighbor_planet_data['name'], neighbor_planet_data['arrival_days'], neighbor_planet_data['path_data'] ))
    #print('\n')

    #print('Planet: {}, old days: {}, new_days: {}'.format(neighbor_planet_data['name'], return_data[current_planet_data['name']][0], return_data[current_planet_data['name']][0] + [neighbor_planet_data['day']] ))
    return_data[neighbor_planet_data['name']] = {
        'arrival_days': neighbor_planet_data['arrival_days'], 
        'hunter_count': neighbor_planet_data['hunter_count'], 
        'path_data': neighbor_planet_data['path_data'], 
        'fuel_level': neighbor_planet_data['fuel']}

    #print('ORIGINAL UPDATE PATH: {}'.format(neighbor_planet_data['path_data']))
    
    # add the neighbor to the list of planets to visit
    heappush(
        planets_to_visit, 
        (
            neighbor_planet_data['hunter_count'],
            neighbor_planet_data['arrival_days'], 
            neighbor_planet_data['fuel'], 
            neighbor_planet_data['name'], 
            current_planet_data['name'],  
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
        path_data[planet] = {
            'arrival_days': [start_day], 
            'hunter_count': inf, 
            'path_data': [{'planet': starting_planet_name, 'arrival_day': start_day, 'hunter_count': 0}], 
            'fuel_level': 0}
    
    # manually set the return paths data for the starting planet
    path_data[starting_planet_name] = {
            'arrival_days': [start_day], 
            'hunter_count': 0, 
            'path_data': [{'planet': starting_planet_name, 'arrival_day': start_day, 'hunter_count': 0}], 
            'fuel_level': fuel_capacity}

    # initialise planets to visit minheap as a list of tuples, containing: 
    # 1. the number of hunters encountered to date 
    # 2. the time in days when arriving at the planet. 
    # 3. the current fuel capacity when arriving at the planet. 
    # 4. the name of the planet
    # 5. the name of the previous planet
    # 6. path to date
    planets_to_visit = [(0, [start_day], fuel_capacity, starting_planet_name, None, [{'planet': starting_planet_name,'arrival_day': start_day, 'hunter_count': 0}])]


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
                'path_data': arrival_path,
                'days_to_neighbor': neighbors_minus_previous[neighbor],
                'refueled': False,
                'waited_for_hunters': False,
                'hunters': arrival_path[-1]['hunter_count']
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
            'arrival_days': arrival_days + [current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor']],
            'day': current_planet_departure_data['day'] + current_planet_departure_data['days_to_neighbor'],
            'fuel': current_planet_departure_data['fuel'] - current_planet_departure_data['days_to_neighbor'],
            'hunter_count': current_planet_departure_data['hunter_count'],
            'hunters': 0
            }
            #print("Looking to travel from {} to {}".format(current_planet_name, neighbor))

            # check whether can reach neighbor withing time limit
            if neighbor_arrival_data['day'] <= time_limit:
                if are_bounty_hunters(galaxy, neighbor_arrival_data['day'], neighbor):
                    neighbor_arrival_data['hunter_count'] += 1
                    neighbor_arrival_data['hunters'] += 1
                    
                #print("neighbor planet path: {}".format(neighbor_arrival_data['path_data']))
                # if less bounty hunters are encountered on this path to the neighbor than a previous checked 
                # path then make this the ideal path to that planet
                if neighbor_arrival_data['hunter_count'] < path_data[neighbor]['hunter_count']:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, galaxy)
                    #print("SUCCESSFUL TRAVEL")
                    
                # if the number of hunters encountered up to arrival at the neighbor is the same as 
                # before, then only update to the current path if the arrival fuel is greater than the 
                # past path. This will cover any case where the current path arrival allows the falcon to 
                # leave the neighbor planet instantly and potentially avoid an extra day hiding from hunters, 
                # while preventing the need to check for hunters at the neighbor or loop through all of the 
                # neighbor's neighbors to check if refuelling is needed
                elif neighbor_arrival_data['hunter_count'] == path_data[neighbor]['hunter_count'] and neighbor_arrival_data['fuel'] > path_data[neighbor]['fuel_level']:
                    updating_fn(path_data, current_planet_departure_data, neighbor_arrival_data, planets_to_visit, galaxy)
                    #print("SUCCESSFUL TRAVEL")
            
                if are_bounty_hunters(galaxy, neighbor_arrival_data['day'], neighbor_arrival_data['name']):
                    #print("TESTING WAIT at {} travelling to {}".format(current_planet_departure_data['name'], neighbor_arrival_data['name']))

                    days_waiting = calculate_wait_time(galaxy, current_planet_departure_data, neighbor_arrival_data, time_limit)

                    #print("Days waiting: {}".format(days_waiting))
                    if days_waiting and neighbor_arrival_data['day'] <= time_limit:
                        #print('waiting and travelling from {} to {}'.format(current_planet_departure_data['name'], neighbor_arrival_data['name']))
                        current_planet_waiting_data = copy.deepcopy(current_planet_departure_data)
                        neighbor_waiting_data = copy.deepcopy(neighbor_arrival_data)
                        neighbor_waiting_data['hunter_count'] -= 1
                        neighbor_waiting_data['hunters'] -= 1

                        
                        departure_day_after_waiting = current_planet_departure_data['day'] + days_waiting
                        neighbor_arrival_day_after_waiting = neighbor_arrival_data['day'] + days_waiting
                        
                        
                        neighbor_waiting_data['day'] = neighbor_arrival_day_after_waiting
                        #print("Arrival days BEFORE: {}".format(neighbor_waiting_data['arrival_days']))
                        neighbor_waiting_data['arrival_days'] = neighbor_waiting_data['arrival_days'][:-1] + [neighbor_arrival_day_after_waiting]
                        #print("Arrival days AFTER: {}".format(neighbor_waiting_data['arrival_days']))
                        
                        
                        current_planet_waiting_data['day'] = departure_day_after_waiting

                        
                        
                        current_planet_waiting_data['waited_for_hunters'] = True
                        
                        
                        current_planet_waiting_data['path_data'][-1]['departure_day'] = current_planet_waiting_data['day']
                        
                        current_planet_waiting_data['path_data'][-1]['waited_for_hunters'] = current_planet_waiting_data['waited_for_hunters']
                        current_planet_waiting_data['path_data'][-1]['hunter_count'] = current_planet_waiting_data['hunters']

                        
                        #refuel while waiting
                        if current_planet_waiting_data['fuel'] < fuel_capacity:
                            current_planet_waiting_data['fuel'] = fuel_capacity
                            current_planet_waiting_data['refueled'] = True
                            neighbor_waiting_data['fuel'] = current_planet_waiting_data['fuel'] - current_planet_waiting_data['days_to_neighbor']
                        current_planet_waiting_data['path_data'][-1]['refueled'] = current_planet_waiting_data['refueled']

                        
                        neighbor_waiting_data['path_data'] = current_planet_waiting_data['path_data'] + [{'planet': neighbor_waiting_data['name'], 'arrival_day': neighbor_waiting_data['day'], 'hunter_count': neighbor_waiting_data['hunters']}]
                        

                        heappush(
                            planets_to_visit, 
                            (
                                neighbor_waiting_data['hunter_count'],
                                neighbor_waiting_data['arrival_days'], 
                                neighbor_waiting_data['fuel'], 
                                neighbor_waiting_data['name'], 
                                current_planet_waiting_data['name'],  
                                neighbor_waiting_data['path_data']))

    
    destination_path_data = path_data[finishing_planet_name]
    odd_of_success = calculate_prob(destination_path_data['hunter_count'])
    
    return_data = {
        'odds': odd_of_success,
        'path_data': destination_path_data['path_data']
    }

    return return_data

if __name__ == '__main__':
    falcon_path = 'flask_backend\galaxies\millennium-falcon-4.json'
    empire_path = 'flask_backend\scenarios\empire-4.json'
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