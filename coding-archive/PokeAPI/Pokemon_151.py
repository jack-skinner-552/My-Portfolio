import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

url = "https://pokeapi.co/api/v2/pokemon?limit=151"
response = requests.get(url)

if response.status_code == 200:
    results = response.json()["results"]

    # Create a blank image with a white background
    width = 800
    height = 96 * len(results)
    img = Image.new("RGB", (width, height), "white")

    # Set the font for the Pokemon names and types
    name_font = ImageFont.truetype("arial.ttf", 20)
    type_font = ImageFont.truetype("arial.ttf", 16)

    # Loop through each Pokemon and add its official artwork, ID, types, and name to the image
    x = 0
    y = 0
    for result in results:
        name = result["name"].capitalize()
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}/'
        pokemon_response = requests.get(pokemon_url)
        pokemon_data = pokemon_response.json()
        pokemon_id = pokemon_data["id"]
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
        name_text = f"{name} ({types_str})"
        id_bbox = draw.textbbox((x + 2, y + 2), id_text, font=type_font)
        id_width = id_bbox[2] - id_bbox[0]
        draw.text((x + 48 - id_width / 2 + 2, y + 2), id_text, font=type_font, fill="black")
        name_bbox = draw.textbbox((x + 48, y + 96), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text((x + 48 - name_width / 2 + 48, y + 96), name_text, font=name_font, fill="black")
        y += 96

    # Save the image to a file
    img.save("pokemon_list.png")

else:
    print("Failed to get Pokemon list.")


