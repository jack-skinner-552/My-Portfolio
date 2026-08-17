import requests
import random
from Pokemon_Type_Colors import TypeColors

while True:
    # Ask for a Pokémon from the user (ex: Venusaur)
    pokemon = input("What is your Pokémon? ")

    # Fetch API Data for Pokémon
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower().replace(' ', '-')}"
    pokemon_types = []
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_types = [t["type"]["name"].capitalize() for t in pokemon_data["types"]]
        type_colored = [TypeColors.colors.get(t, "\033[0m") + t + "\033[0m" for t in pokemon_types]
        print(f"Your {pokemon} is a {'/'.join(type_colored)} Type Pokémon")
        break
    else:
        print(f"{pokemon} is not a valid Pokémon choice. Please try again.")

while True:
    # Ask what the opponent's move is from the user (ex: Flamethrower)
    move = input("What is your opponent's move? ")

    # Fetch API Data for Move
    move_url = f"https://pokeapi.co/api/v2/move/{move.lower().replace(' ', '-')}"
    response = requests.get(move_url)
    if response.status_code == 200:
        move_data = response.json()
        move_type = move_data["type"]["name"].capitalize()
        move_ailment_chance, move_crit_rate, move_flinch_rate = 0, 0, 0
        move_ailment = "none"
        if move_data["meta"]:
            move_ailment = move_data["meta"]["ailment"]["name"]
            move_ailment_chance = move_data["meta"]["ailment_chance"]/100
            move_crit_rate = move_data["meta"]["crit_rate"]/100
            move_flinch_rate = move_data.get("meta", {}).get("flinch_chance", 0)/100
        color_code = TypeColors.colors.get(move_type, "\033[0m")
        print(f"{move} is a {color_code}{move_type}\033[0m type move")

        # Fetch API Data for Move Type
        type_url = f"https://pokeapi.co/api/v2/type/{move_type.lower()}"
        response = requests.get(type_url)
        type_data = response.json()
        type_strengths = type_data["damage_relations"]["double_damage_to"]
        type_strengths_names = [strength["name"].capitalize() for strength in type_strengths]
        type_weaknesses = type_data["damage_relations"]["half_damage_to"]
        type_weakness_names = [weakness["name"].capitalize() for weakness in type_weaknesses]
        type_no_damage = type_data["damage_relations"]["no_damage_to"]
        type_no_damage_names = [no_damage["name"].capitalize() for no_damage in type_no_damage]

        # If move has a crit_rate, print Critical Hit if Random # between 0 & 1 is less than the move's crit_rate
        if random.random() < move_crit_rate:
            print("Critical Hit!")

        # Print whether the move is Super Effective, Not Very Effective, Does No Damage, or Does Normal Damage
        if (any(pokemon_type in type_strengths_names for pokemon_type in pokemon_types)
                and not any(pokemon_type in type_weakness_names for pokemon_type in pokemon_types)
                and not any(pokemon_type in type_no_damage_names for pokemon_type in pokemon_types)):
            print(f"{move} is Super Effective Against {pokemon}.")
        elif (any(pokemon_type in type_weakness_names for pokemon_type in pokemon_types)
              and not any(pokemon_type in type_strengths_names for pokemon_type in pokemon_types)
              and not any(pokemon_type in type_no_damage_names for pokemon_type in pokemon_types)):
            print(f"{move} is Not Very Effective Against {pokemon}.")
        elif any(pokemon_type in type_no_damage_names for pokemon_type in pokemon_types):
            print(f"{move} Doesn't Affect {pokemon}")
        else:
            print(f"{move} Does Normal Damage to {pokemon}")

        # If move has an ailment, print ailment if Random # between 0 & 1 is less than ailment_chance
        if random.random() < move_ailment_chance:
            if move_ailment == ('burn' or 'poison'):
                print(f"Your {pokemon} has been {move_ailment}ed!")
            if move_ailment == 'confusion':
                print(f"Your {pokemon} is Confused!")
            if move_ailment == 'freeze':
                print(f"Your {pokemon} is Frozen!")
            if move_ailment == 'paralysis':
                print(f"Your {pokemon} is Paralyzed!")

        # If move has a flinch_rate, print flinch if Random # between 0 & 1 is less than flinch_rate
        if random.random() < move_flinch_rate:
            print(f"Your {pokemon} flinched!")
        break
    else:
        print(f"{move} is not a valid Pokémon move. Please try again.")
