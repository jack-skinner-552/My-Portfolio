# Program asks for a Pokemon Move Ailment and displays the moves that can cause the ailment

import requests

# Get the move ailment from the user
ailment = input("Enter a move ailment name: ")

# The PokeAPI URL for the move ailment
ailment_url = "https://pokeapi.co/api/v2/move-ailment/" + ailment.lower()

# Make an API request to retrieve ailment
response = requests.get(ailment_url)

# If the request was successful (status code of 200)
if response.status_code == 200:
    # Extract the list of moves from the response
    ailment_data = response.json()
    move_list = [move["name"] for move in ailment_data["moves"]]

    # Print the moves that can cause input ailment
    print(f"{ailment} moves:")
    #print(pokemon_list)
    for move in move_list:
        print(move)
        
else:
    print("Error retrieving list of Moves from PokeAPI")