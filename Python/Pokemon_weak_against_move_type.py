import requests

# Get the move type from the user
move_type = input("Enter a move type: ")

# The PokeAPI URL for the move type
move_type_url = "https://pokeapi.co/api/v2/type/" + move_type.lower()

# Make an API request to retrieve information about the move type
response = requests.get(move_type_url)

# If the request was successful (status code of 200)
if response.status_code == 200:
    # Extract the list of Pokemon that are weak to input type moves
    type_data = response.json()
    type_strengths = type_data["damage_relations"]["double_damage_to"]
    type_strengths_names = [strength["name"] for strength in type_strengths]
    type_weaknesses = type_data["damage_relations"]["half_damage_to"]
    type_weakness_names = [weakness["name"] for weakness in type_weaknesses]
    type_no_damage = type_data["damage_relations"]["no_damage_to"]
    type_no_damage_names = [no_damage["name"] for no_damage in type_no_damage]

    print(move_type, "is strong against", type_strengths_names)
    print(move_type, "is weak against", type_weakness_names)
    if type_no_damage_names:
        print(move_type, "does no damage to", type_no_damage_names)

    # Make an API request to retrieve information about all Pokemon
    all_pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=1118"
    response = requests.get(all_pokemon_url)

    # If the request was successful (status code of 200)
    if response.status_code == 200:
        # Extract the list of all Pokemon
        all_pokemon_data = response.json()
        all_pokemon_list = all_pokemon_data["results"]

        # Make a list of Pokemon that are weak to input type moves
        type_weak_pokemon = []
        for pokemon in all_pokemon_list:
            pokemon_url = pokemon["url"]
            pokemon_response = requests.get(pokemon_url)
            pokemon_data = pokemon_response.json()
            pokemon_id = pokemon_data["id"]
            pokemon_types = [type["type"]["name"] for type in pokemon_data["types"]]
            if set(type_strengths_names) & set(pokemon_types):
                if not set(type_weakness_names) & set(pokemon_types):
                    if not set(type_no_damage_names) & set(pokemon_types):
                        type_weak_pokemon.append((pokemon_id, pokemon["name"], pokemon_types))

        # Sort the list of weak Pokemon by ID number
        type_weak_pokemon.sort()

        # Print the names of the weak Pokemon, their ID numbers, and their types
        print(f"Pokemon weak to {move_type} moves:")
        for pokemon in type_weak_pokemon:
            print(f'{pokemon[0]}: {pokemon[1].capitalize()} Types: {pokemon[2]}')
    else:
        print("Error retrieving information about all Pokemon from PokeAPI")
else:
    print("Error retrieving information about the move type from PokeAPI")