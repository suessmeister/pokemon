from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import random
import requests
from io import BytesIO
import math
import os

# Pokemon card colors for different types
TYPE_COLORS = {
    "fire": ("#FB6C6C", "#FFB7B7"),    # Red gradient
    "water": ("#76BEFE", "#B8DFFF"),   # Blue gradient
    "grass": ("#48D0B0", "#9DFFD9"),   # Green gradient
    "electric": ("#FFD86F", "#FFF4D1"), # Yellow gradient
    "ice": ("#9EDEFB", "#D1F3FF"),     # Light blue gradient
    "fighting": ("#C03028", "#FFB7B7"), # Dark red gradient
    "poison": ("#A040A0", "#E5B8E5"),  # Purple gradient
    "ground": ("#E0C068", "#F5E6D3"),  # Brown gradient
    "flying": ("#A890F0", "#D1C8FF"),  # Light purple gradient
    "psychic": ("#F85888", "#FFBCD4"), # Pink gradient
    "bug": ("#A8B820", "#D9E68C"),     # Lime gradient
    "rock": ("#B8A038", "#E6D5A7"),    # Beige gradient
    "ghost": ("#705898", "#B8A7D0"),   # Dark purple gradient
    "dragon": ("#7038F8", "#B49EFF"),  # Indigo gradient
    "dark": ("#705848", "#B3A598"),    # Gray gradient
    "steel": ("#B8B8D0", "#E5E5F0"),   # Silver gradient
    "fairy": ("#EE99AC", "#FFD1DC")    # Light pink gradient
}

# Create fonts directory if it doesn't exist
FONTS_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
os.makedirs(FONTS_DIR, exist_ok=True)

def get_fonts():
    """Get the font objects for different text elements"""
    # Using Arial as a fallback since it's commonly available
    try:
            title_font = ImageFont.truetype('arial.ttf', 60)
            name_font = ImageFont.truetype('arial.ttf', 45)
            stats_font = ImageFont.truetype('arial.ttf', 36)
            attack_name_font = ImageFont.truetype('arial.ttf', 40)
            attack_damage_font = ImageFont.truetype('arialbd.ttf', 45)
    except Exception as e:
            print(f"Warning: Could not load system fonts ({str(e)}). Using default font.")
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            stats_font = ImageFont.load_default()
            attack_name_font = ImageFont.load_default()
            attack_damage_font = ImageFont.load_default()
    
    return {
        'title': title_font,
        'name': name_font,
        'stats': stats_font,
        'attack_name': attack_name_font,
        'attack_damage': attack_damage_font
    }

def create_card_background(img, pokemon_type, width, height):
    draw = ImageDraw.Draw(img)
    
    # Get type colors for gradient
    primary_color, secondary_color = TYPE_COLORS.get(pokemon_type.lower(), ("#FFFFFF", "#EEEEEE"))
    
    # Create a gradient background
    for y in range(height):
        # Calculate color for this line
        ratio = y / height
        r = int(int(primary_color[1:3], 16) * (1 - ratio) + int(secondary_color[1:3], 16) * ratio)
        g = int(int(primary_color[3:5], 16) * (1 - ratio) + int(secondary_color[3:5], 16) * ratio)
        b = int(int(primary_color[5:7], 16) * (1 - ratio) + int(secondary_color[5:7], 16) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        draw.line([(0, y), (width, y)], fill=color)

def create_card_frame(img, width, height):
    draw = ImageDraw.Draw(img)
    
    # Inner card frame (golden border)
    border_color = "#DAA520"
    border_width = 8
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=border_color,
        width=border_width
    )
    
    # Add some shine effects
    shine_colors = ['#FFD700', '#FDB931', '#FFE5B4']
    for i in range(0, width, 10):
        color = random.choice(shine_colors)
        if random.random() > 0.7:  # Only add shine sometimes
            draw.line([(i, 0), (i + 5, 0)], fill=color, width=2)
            draw.line([(i, height - 1), (i + 5, height - 1)], fill=color, width=2)

def get_pokemon_image(pokemon_name):
    """Fetch Pokemon image from PokeAPI"""
    try:
        pokemon_name = pokemon_name.lower()
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()
            artwork_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
            image_response = requests.get(artwork_url)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print("error")
    return None

def create_nft_card(name, pokemon_type, attack, defense, hp, attacks):
    # Pokemon card dimensions (scaled up from standard size)
    width = 750  # 2.5" * 300dpi
    height = 1050  # 3.5" * 300dpi
    
    # Create base image
    img = Image.new("RGBA", (width, height), color="white")
    
    # Add type-based gradient background
    create_card_background(img, pokemon_type, width, height)
    
    # Add card frame
    create_card_frame(img, width, height)
    
    draw = ImageDraw.Draw(img)
    
    # Get fonts
    fonts = get_fonts()
    
    # Pokemon name and HP
    draw.text((50, 40), name.upper(), font=fonts['name'], fill="black")
    
    # HP text with larger bold font
    hp_text = f"HP {hp}"
    hp_width = fonts['title'].getlength(hp_text)
    draw.text((width - hp_width - 50, 40), hp_text, font=fonts['title'], fill="red")
    
    # Pokemon image
    pokemon_img = get_pokemon_image(name)
    if pokemon_img:
        pokemon_img = pokemon_img.convert('RGBA')
        # Make image area larger
        pokemon_size = (400, 400)
        pokemon_img = pokemon_img.resize(pokemon_size)
        
        # Add a subtle shadow effect
        shadow = Image.new('RGBA', pokemon_img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse([0, pokemon_size[1] - 20, pokemon_size[0], pokemon_size[1]], fill=(0, 0, 0, 100))
        
        # Calculate center position
        img_x = (width - pokemon_size[0]) // 2
        img_y = 100
        
        # Paste shadow and image
        img.paste(shadow, (img_x, img_y), shadow)
        img.paste(pokemon_img, (img_x, img_y), pokemon_img)
    
    # Type symbol
    type_circle_center = (60, 520)
    type_circle_radius = 25
    draw.ellipse(
        [
            type_circle_center[0] - type_circle_radius,
            type_circle_center[1] - type_circle_radius,
            type_circle_center[0] + type_circle_radius,
            type_circle_center[1] + type_circle_radius
        ],
        fill=TYPE_COLORS[pokemon_type.lower()][0]
    )
    
    # Stats bar with proper font
    stats_y = 560
    draw.text((50, stats_y), f"Attack:  {attack}", font=fonts['stats'], fill="black")
    draw.text((50, stats_y + 30), f"Defense: {defense}", font=fonts['stats'], fill="black")
    
    # Attacks with improved typography
    attack_y = 650
    for i, (attack_name, attack_damage) in enumerate(attacks):
        # Attack background
        draw.rectangle(
            [(40, attack_y), (width - 40, attack_y + 60)],
            fill=TYPE_COLORS[pokemon_type.lower()][1],
            outline=TYPE_COLORS[pokemon_type.lower()][0],
            width=2
        )
        
        # Attack text with proper fonts
        draw.text((60, attack_y + 10), attack_name, font=fonts['attack_name'], fill="black")
        
        # Right-aligned damage number
        damage_text = str(attack_damage)
        damage_width = fonts['attack_damage'].getlength(damage_text)
        draw.text((width - damage_width - 60, attack_y + 10), damage_text, font=fonts['attack_damage'], fill="black")
        
        attack_y += 80
    
    # Add a subtle texture overlay
    texture = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    texture_draw = ImageDraw.Draw(texture)
    for i in range(0, width, 4):
        for j in range(0, height, 4):
            if random.random() > 0.5:
                texture_draw.point((i, j), fill=(255, 255, 255, 5))
    
    img = Image.alpha_composite(img.convert('RGBA'), texture)
    
    # Add a subtle glow effect
    glow = img.filter(ImageFilter.GaussianBlur(2))
    img = Image.blend(img, glow, 0.1)
    
    # Convert to RGB for saving
    img = img.convert('RGB')
    
    # Ensure mons directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '../../public/mons'), exist_ok=True)
    
    # Save image in mons directory
    save_path = os.path.join(os.path.dirname(__file__), '../../public/mons', f"{name}_nft.png")
    img.save(save_path, quality=95)
    print(f"NFT card saved as {save_path}")
    return save_path
