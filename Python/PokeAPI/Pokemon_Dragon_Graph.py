import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Make a GET request to the PokeAPI endpoint that returns information about dragon type Pokemon
response = requests.get('https://pokeapi.co/api/v2/type/dragon')

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

    # Filter the results to only include default dragon type Pokemon & Add them to Image
    x = 0
    y = 0
    dragon_pokemon = []
    for pokemon in data['pokemon']:
        pokemon_url = pokemon['pokemon']['url']
        pokemon_data = requests.get(pokemon_url).json()
        if pokemon_data['is_default'] and any(type_info['type']['name'] == 'dragon' for type_info in pokemon_data['types']):
            pokemon_id = pokemon_data['id']
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
            dragon_pokemon.append({'id': pokemon_id, 'name': pokemon_name, 'types': types})

        new_height = len(dragon_pokemon) * 96
        n_img = img.crop((0, 0, width, new_height))

        n_img.save("pokemon_list.png")

    # Print the list of default dragon type Pokemon
    for pokemon in dragon_pokemon:
        print(f"ID: {pokemon['id']} | Name: {pokemon['name']} | Types: {', '.join(pokemon['types'])}")

else:
    print("Failed to get Pokemon list.")
