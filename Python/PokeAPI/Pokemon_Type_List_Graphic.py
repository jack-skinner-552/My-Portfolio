# Pokemon_Type_List_Graphic.py

# This program gets a Pokemon Type from user input, then creates an image
# listing all the Pokemon that belongs to that type up to Generation VIII
import requests
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


def get_pokemon_list(p_type):
    # The PokeAPI URL for the Pokemon Type
    type_url = 'https://pokeapi.co/api/v2/type/' + p_type.lower()

    # Make a GET request to the PokeAPI endpoint that returns information about input type Pokemon
    response = requests.get(type_url)

    # If the request was successful, extract the JSON data from the response
    if response.status_code == 200:
        data = response.json()

        pokemon_urls = [pokemon['pokemon']['url'] for pokemon in data['pokemon'] if int(pokemon['pokemon']['url'].split('/')[-2]) <= 905]
        pokemon_data = [requests.get(url).json() for url in tqdm(pokemon_urls, desc="Fetching Pokemon Data")]

        type_pokemon = []
        for pokemon in pokemon_data:
            if any(type_info['type']['name'] == p_type.lower() for type_info in pokemon['types']):
                pokemon_id = pokemon['id']
                pokemon_name = pokemon['name']
                types = [t["type"]["name"] for t in pokemon["types"]]
                types = [t.capitalize() for t in types]
                type_pokemon.append({'id': pokemon_id, 'name': pokemon_name.capitalize(), 'types': types})

        n_pokemon = len(type_pokemon)
        print(f'There are {n_pokemon} {p_type} type Pokemon.')
        for pokemon in type_pokemon:
            print(f"ID: {pokemon['id']} | Name: {pokemon['name']} | Types: {', '.join(pokemon['types'])}")

        return type_pokemon
    else:
        print("Failed to get Pokemon list.")
        return None


def create_pokemon_image(type_pokemon, p_type):
    # Create a blank image with a white background
    width = 800
    height = 96 * len(type_pokemon) + 48
    img = Image.new("RGB", (width, height), "white")

    # Set the font for the Pokemon names and types
    name_font = ImageFont.truetype("arial.ttf", 20)
    type_font = ImageFont.truetype("arial.ttf", 16)

    # Draw the heading
    draw = ImageDraw.Draw(img)
    heading_text = f"All {p_type} Type Pokémon"
    heading_font = ImageFont.truetype("arial.ttf", 24)
    heading_bbox = draw.textbbox((0, 0), heading_text, font=heading_font, align="center")
    heading_width = heading_bbox[2] - heading_bbox[0]
    draw.text(((width - heading_width) / 2, 0), heading_text, font=heading_font, fill="black", align="center")

    # Add the Pokemon sprites and information to the image
    x = 0
    y = 0
    for pokemon in tqdm(type_pokemon, desc="Creating List Image"):
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png"
        sprite_response = requests.get(sprite_url)
        sprite_data = sprite_response.content
        sprite_img = Image.open(BytesIO(sprite_data))
        sprite_img = sprite_img.resize((96, 96))
        img.paste(sprite_img, (x, y))
        draw = ImageDraw.Draw(img)
        types_str = "/".join(pokemon['types'])
        id_text = f"#{pokemon['id']}"
        name_text = f"{pokemon['name']} ({types_str})"
        id_bbox = draw.textbbox((x + 2, y + 36), id_text, font=type_font)
        id_width = id_bbox[2] - id_bbox[0]
        draw.text((x + 48 - id_width / 2 + 200, y + 36), id_text, font=type_font, fill="black")
        name_bbox = draw.textbbox((x + 48, y + 36), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text((x + 48 - name_width / 2 + 480, y + 36), name_text, font=name_font, fill="black")
        draw.line((0, y, width, y), fill="black")
        y += 96

    img_file = "pokemon_list_" + p_type.lower() + ".png"
    img.save(img_file)
    os.startfile(img_file)


def main():
    # Get the Pokemon Type from the user
    p_type = input("Enter a Pokemon Type: ")
    create_pokemon_image(get_pokemon_list(p_type), p_type)


if __name__ == "__main__":
    main()
