import sys
from galaxy_structure import generate_galaxy, reveal_bounty_hunters, open_json
from millenium_falcon_mainframe import calculate_path

if __name__ == "__main__":
    falcon_path = sys.argv[1]
    falcon_data = open_json(falcon_path)
    empire_data = open_json(sys.argv[2])
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

    print(optimal_path_data['odds'])