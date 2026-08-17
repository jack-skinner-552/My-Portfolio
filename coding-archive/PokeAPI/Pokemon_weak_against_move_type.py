# Program asks for a Pokemon Type and displays the pokemon who are weak against given type moves.

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from tqdm import tqdm
import requests
import os


def get_pokemon_list(m_type):
    # The PokeAPI URL for the move type
    move_type_url = "https://pokeapi.co/api/v2/type/" + m_type.lower()

    # Make an API request to retrieve information about the move type
    response = requests.get(move_type_url)

    # If the request was successful (status code of 200)
    if response.status_code == 200:
        # Extract the lists of Pokemon types that are weak against, strong against, and immune to input type moves
        type_data = response.json()
        type_strengths = type_data["damage_relations"]["double_damage_to"]
        type_strengths_names = [strength["name"] for strength in type_strengths]
        type_weaknesses = type_data["damage_relations"]["half_damage_to"]
        type_weakness_names = [weakness["name"] for weakness in type_weaknesses]
        type_no_damage = type_data["damage_relations"]["no_damage_to"]
        type_no_damage_names = [no_damage["name"] for no_damage in type_no_damage]

        # Print the Types the Input is strong against, weak against, and immune to
        if type_strengths_names:
            print(m_type, "is strong against", type_strengths_names)
        print(m_type, "is weak against", type_weakness_names)
        if type_no_damage_names:
            print(m_type, "does no damage to", type_no_damage_names)

        # If "Normal" is the Input, print one line and end program
        if m_type.lower() == "normal":
            print("There are no Pokémon who are weak to Normal moves.")
            return []
        else:
            type_weak_pokemon = []
            # Make an API request to retrieve information about all Pokemon types
            for pokemon_type in tqdm(type_strengths_names, desc="Fetching Pokemon Data"):
                url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    pokemon_urls = [p['pokemon']['url'] for p in data['pokemon'] if int(p['pokemon']['url'].split('/')[-2]) <= 905]
                    pokemon_data = [requests.get(u).json() for u in pokemon_urls]
                    for p in pokemon_data:
                        try:
                            name = p["name"].capitalize()
                            id = p["id"]
                            types = [t["type"]["name"] for t in p["types"]]
                            if not set(type_weakness_names) & set(types):
                                if not set(type_no_damage_names) & set(types):
                                    if {'id': id, 'name': name, 'types': types} not in type_weak_pokemon:
                                        type_weak_pokemon.append({'id': id, 'name': name, 'types': types})
                        except KeyError:
                            continue

            # Sort the list of weak Pokemon by ID
            type_weak_pokemon.sort(key=lambda x: int(x["id"]))

            # Print the names of the weak Pokemon, their ID numbers, and their types
            print(f"Pokémon weak to {m_type} moves:")
            for pokemon in type_weak_pokemon:
                print(f"ID: {pokemon['id']} | Name: {pokemon['name']} | Types: {', '.join(pokemon['types'])}")

            return type_weak_pokemon

    else:
        print("Error retrieving information about the move type from PokeAPI")
        return []


def create_pokemon_image(pokemon_list, m_type):
    # Create a blank image with a white background
    width = 800
    height = 96 * len(pokemon_list) + 48
    img = Image.new("RGB", (width, height), "white")

    # Set the font for the Pokemon names and types
    name_font = ImageFont.truetype("arial.ttf", 20)
    type_font = ImageFont.truetype("arial.ttf", 16)

    # Draw the heading
    draw = ImageDraw.Draw(img)
    h_text = f"All Pokémon Who Are Weak Against {m_type} Moves ({len(pokemon_list)})"
    heading_font = ImageFont.truetype("arial.ttf", 24)
    heading_bbox = draw.textbbox((0, 0), h_text, font=heading_font, align="center")
    heading_width = heading_bbox[2] - heading_bbox[0]
    draw.text(((width - heading_width) / 2, 0), h_text, font=heading_font, fill="black", align="center")

    # Add the Pokémon sprites and information to the image
    x = 0
    y = 48
    for pokemon in tqdm(pokemon_list, desc="Creating List Image"):
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

    img_file = "pokemon_weak_against_" + m_type.lower() + "_moves1.png"
    img.save(img_file)
    os.startfile(img_file)  # Open the image file using the default application


def main():
    # Get the move type from the user
    move_type = input("Enter a move type: ")
    create_pokemon_image(get_pokemon_list(move_type), move_type)


if __name__ == "__main__":
    main()
