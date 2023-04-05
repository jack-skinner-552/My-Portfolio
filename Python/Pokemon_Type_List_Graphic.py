# This program gets a Pokemon Type from user input, then creates an image listing all the Pokemon that belongs to that type up to Generation VIII

import requests
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Get the Pokemon Type from the user
p_type = input('Enter a Pokemon Type: ')

# The PokeAPI URL for the Pokemon Type
type_url = 'https://pokeapi.co/api/v2/type/' + p_type.lower()

# Make a GET request to the PokeAPI endpoint that returns information about input type Pokemon
response = requests.get(type_url)

# If the request was successful, extract the JSON data from the response
if response.status_code == 200:
    data = response.json()

    # Create a blank image with a white background
    width = 800
    height = 96 * len(data['pokemon'])
    img = Image.new("RGB", (width, height), "white")

    # Set the font for the Pokemon names and types
    name_font = ImageFont.truetype("arial.ttf", 20)
    type_font = ImageFont.truetype("arial.ttf", 16)

    # Filter the results to only include default input type Pokemon & Add them to Image
    x = 0
    y = 0
    type_pokemon = []
    for pokemon in tqdm(data['pokemon']):
        pokemon_url = pokemon['pokemon']['url']
        pokemon_data = requests.get(pokemon_url).json()
        if pokemon_data['is_default'] and any(type_info['type']['name'] == p_type.lower() for type_info in pokemon_data['types']):
            pokemon_id = pokemon_data['id']
            # Generation IX Pokemon ID information in PokeAPI is currently incorrect, for now, only include Generations I-VIII
            if pokemon_id <= 905:
                pokemon_name = pokemon_data['name'].capitalize()
                sprite_url = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
                sprite_response = requests.get(sprite_url)
                sprite_data = sprite_response.content
                sprite_img = Image.open(BytesIO(sprite_data))
                sprite_img = sprite_img.resize((96, 96))
                img.paste(sprite_img, (x, y))
                draw = ImageDraw.Draw(img)
                types = [t["type"]["name"].capitalize() for t in pokemon_data["types"]]
                types_str = "/".join(types)
                id_text = f"#{pokemon_id}"
                name_text = f"{pokemon_name} ({types_str})"
                id_bbox = draw.textbbox((x + 2, y + 36), id_text, font=type_font)
                id_width = id_bbox[2] - id_bbox[0]
                draw.text((x + 48 - id_width / 2 + 200, y + 36), id_text, font=type_font, fill="black")
                name_bbox = draw.textbbox((x + 48, y + 36), name_text, font=name_font)
                name_width = name_bbox[2] - name_bbox[0]
                draw.text((x + 48 - name_width / 2 + 480, y + 36), name_text, font=name_font, fill="black")
                draw.line((0,y,width,y), fill="black")
                y += 96
                type_pokemon.append({'id': pokemon_id, 'name': pokemon_name, 'types': types})

        n_pokemon = len(type_pokemon)

        # Any unused space in the image is cropped out, and the final image is saved
        new_height = n_pokemon * 96
        new_img = img.crop((0, 0, width, new_height))
        new_img.save("pokemon_list_" + p_type.lower() +".png")

    # Print the list of input type Pokemon
    print(f'There are {n_pokemon} {p_type} type Pokemon.')
    for pokemon in type_pokemon:
        print(f"ID: {pokemon['id']} | Name: {pokemon['name']} | Types: {', '.join(pokemon['types'])}")

else:
    print("Failed to get Pokemon list.")
