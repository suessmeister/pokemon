from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import requests
from io import BytesIO
import math
import os

# Type to light color mapping for readable backgrounds
TYPE_COLORS = {
    "fire": "#FFE5E5",    # Light red
    "water": "#E5F6FF",   # Light blue
    "grass": "#E8FFE5",   # Light green
    "electric": "#FFFDE5", # Light yellow
    "ice": "#F0FFFF",     # Light cyan
    "fighting": "#FFE5E5", # Light red-pink
    "poison": "#F8E5FF",  # Light purple
    "ground": "#F5E6D3",  # Light brown
    "flying": "#F0F8FF",  # Light sky blue
    "psychic": "#FFE5F7", # Light pink
    "bug": "#F0FFE5",     # Light lime
    "rock": "#F5F5DC",    # Light beige
    "ghost": "#F2E5FF",   # Light violet
    "dragon": "#E5EEFF",  # Light indigo
    "dark": "#E5E5E5",    # Light gray
    "steel": "#F5F5F5",   # Light silver
    "fairy": "#FFE5F5"    # Light magenta
}

def create_glitter_border(img, width, height):
    draw = ImageDraw.Draw(img)
    
    # Metallic gold colors for glitter effect
    gold_colors = ['#FFD700', '#FDB931', '#FFDF00', '#DAA520', '#FFE5B4']
    
    # Draw border segments with different gold shades
    for i in range(0, width, 5):  # Top and bottom borders
        color = random.choice(gold_colors)
        # Top border
        draw.line([(i, 0), (min(i + 5, width - 1), 0)], fill=color, width=2)
        # Bottom border
        draw.line([(i, height - 1), (min(i + 5, width - 1), height - 1)], fill=color, width=2)
    
    for i in range(0, height, 5):  # Left and right borders
        color = random.choice(gold_colors)
        # Left border
        draw.line([(0, i), (0, min(i + 5, height - 1))], fill=color, width=2)
        # Right border
        draw.line([(width - 1, i), (width - 1, min(i + 5, height - 1))], fill=color, width=2)

def get_pokemon_image(pokemon_name):
    """Fetch Pokemon image from PokeAPI"""
    try:
        # Convert pokemon name to lowercase for API
        pokemon_name = pokemon_name.lower()
        # Get Pokemon data from PokeAPI
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()
            # Get the official artwork URL
            artwork_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
            # Download the image
            image_response = requests.get(artwork_url)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print(f"Could not fetch Pokemon image: {e}")
    return None

def create_nft_card(name, pokemon_type, attack, defense, hp, attacks):
    width = 300
    height = 450
    
    # Create image with type-based background color
    background_color = TYPE_COLORS.get(pokemon_type.lower(), "white")
    img = Image.new("RGBA", (width, height), color=background_color)  # Create as RGBA initially
    
    # Add glittering border
    create_glitter_border(img, width, height)
    
    draw = ImageDraw.Draw(img)

    # Load default font (you can change it to a custom font if needed)
    font = ImageFont.load_default()

    # Title (name of the NFT)
    title_font = ImageFont.load_default()
    draw.text((20, 20), f"{name}", font=title_font, fill="black")
    
    # Add Pokemon image
    pokemon_img = get_pokemon_image(name)
    if pokemon_img:
        # Convert to RGBA to ensure transparency support
        pokemon_img = pokemon_img.convert('RGBA')
        # Resize the pokemon image to fit the card (150x150 pixels)
        pokemon_img = pokemon_img.resize((150, 150))
        # Calculate center position for the image
        img_x = (width - 150) // 2
        img_y = 50
        # Directly paste the image with transparency
        img.paste(pokemon_img, (img_x, img_y), pokemon_img)
    
    # Recreate draw object after pasting image
    draw = ImageDraw.Draw(img)
    
    # Type (moved below image)
    draw.text((20, 220), f"Type: {pokemon_type}", font=font, fill="black")

    # Stats
    draw.text((20, 250), f"Attack: {attack}", font=font, fill="black")
    draw.text((20, 280), f"Defense: {defense}", font=font, fill="black")
    draw.text((20, 310), f"HP: {hp}", font=font, fill="black")

    # Attacks
    attack_y = 340
    for i, (attack_name, attack_damage) in enumerate(attacks):
        draw.text((20, attack_y), f"Attack {i+1}: {attack_name} ({attack_damage} damage)", font=font, fill="black")
        attack_y += 40

    # Convert to RGB for saving
    img = img.convert('RGB')
    
    # Ensure mons directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '../../mons'), exist_ok=True)
    
    # Save image in mons directory
    save_path = os.path.join(os.path.dirname(__file__), '../../mons', f"{name}_nft.png")
    img.save(save_path)
    print(f"NFT card saved as {save_path}")
    return save_path

def clean_mons_directory():
    """Remove all files from the mons directory"""
    mons_dir = os.path.join(os.path.dirname(__file__), '../../mons')
    if os.path.exists(mons_dir):
        shutil.rmtree(mons_dir)
        print(f"Cleaned up {mons_dir}")
