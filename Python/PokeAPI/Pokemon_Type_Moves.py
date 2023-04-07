# Program asks for a Pokemon Type and displays the moves that belong to the given type.

import requests

# Get the move type from the user
p_type = input("Enter a move type: ")

# The PokeAPI URL for the move type
type_url = "https://pokeapi.co/api/v2/type/" + p_type.lower()

# Make an API request to retrieve dragon type
response = requests.get(type_url)

# If the request was successful (status code of 200)
if response.status_code == 200:
    # Extract the list of Pokemon from the response
    type_data = response.json()
    move_list = type_data["moves"]
    

    # Print the names of the Dragon Pokemon
    print(f"{p_type} moves:")
    #print(pokemon_list)
    for move in move_list:
        
        print(move["name"])
else:
    print("Error retrieving list of Moves from PokeAPI")