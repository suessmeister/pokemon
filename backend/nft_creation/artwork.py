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

# Pokemon font file path
HOLLOW_FONT = os.path.join(FONTS_DIR, 'Pokemon Hollow.ttf')
SOLID_FONT = os.path.join(FONTS_DIR, 'Pokemon Solid.ttf')
TEXT_FONT = os.path.join(FONTS_DIR, 'ShortBaby-Mg2w.ttf')

def get_fonts():
    """Get the font objects for different text elements"""
    try:
        # Use Pokemon font with increased sizes
        title_font = ImageFont.truetype(SOLID_FONT, 40)
        name_font = ImageFont.truetype(SOLID_FONT, 70)
        stats_font = ImageFont.truetype(HOLLOW_FONT, 30)
        attack_name_font = ImageFont.truetype(HOLLOW_FONT, 50)
        attack_damage_font = ImageFont.truetype(SOLID_FONT, 50)
    except Exception as e:
        print(f"Warning: Could not load Pokemon font ({str(e)}). Using system font.")
        try:
            # Fallback to system font
            title_font = ImageFont.truetype('arial.ttf', 80)
            name_font = ImageFont.truetype('arial.ttf', 65)
            stats_font = ImageFont.truetype('arial.ttf', 50)
            attack_name_font = ImageFont.truetype('arial.ttf', 120)
            attack_damage_font = ImageFont.truetype('arial.ttf', 130)
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
    radius = 20  # Corner radius
    
    # Draw rounded rectangle for the border
    # Top-left corner
    draw.arc([(border_width, border_width), 
              (border_width + radius*2, border_width + radius*2)], 
             180, 270, fill=border_color, width=border_width)
    # Top-right corner
    draw.arc([(width - border_width - radius*2, border_width), 
              (width - border_width, border_width + radius*2)], 
             270, 0, fill=border_color, width=border_width)
    # Bottom-right corner
    draw.arc([(width - border_width - radius*2, height - border_width - radius*2), 
              (width - border_width, height - border_width)], 
             0, 90, fill=border_color, width=border_width)
    # Bottom-left corner
    draw.arc([(border_width, height - border_width - radius*2), 
              (border_width + radius*2, height - border_width)], 
             90, 180, fill=border_color, width=border_width)
    
    # Draw straight lines between corners
    # Top
    draw.line([(border_width + radius, border_width), 
               (width - border_width - radius, border_width)], 
              fill=border_color, width=border_width)
    # Right
    draw.line([(width - border_width, border_width + radius), 
               (width - border_width, height - border_width - radius)], 
              fill=border_color, width=border_width)
    # Bottom
    draw.line([(border_width + radius, height - border_width), 
               (width - border_width - radius, height - border_width)], 
              fill=border_color, width=border_width)
    # Left
    draw.line([(border_width, border_width + radius), 
               (border_width, height - border_width - radius)], 
              fill=border_color, width=border_width)
    
    # Add some shine effects
    # shine_colors = ['#FFD700', '#FDB931', '#FFE5B4']
    # for i in range(0, width, 10):
    #     color = random.choice(shine_colors)
    #     if random.random() > 0.7:  # Only add shine sometimes
    #         draw.line([(i, 0), (i + 5, 0)], fill=color, width=2)
    #         draw.line([(i, height - 1), (i + 5, height - 1)], fill=color, width=2)

def get_pokemon_image(pokemon_name, shiny=False):
    """Fetch Pokemon image from PokeAPI"""
    try:
        pokemon_name = pokemon_name.lower()
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()
            if shiny:
                artwork_url = pokemon_data['sprites']['other']['official-artwork']['front_shiny']
            else:
                artwork_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
            image_response = requests.get(artwork_url)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print(f"Error fetching Pokemon image: {str(e)}")
    return None

def create_nft_card(pokemon, output_dir='../../public/mons'):
    # Pokemon card dimensions (scaled up from standard size)
    width = 750  # 2.5" * 300dpi
    height = 1050  # 3.5" * 300dpi
    
    # Create base image
    img = Image.new("RGBA", (width, height), color="white")
    
    # Add type-based gradient background
    create_card_background(img, pokemon["type"], width, height)
    
    # Add card frame
    create_card_frame(img, width, height)
    
    # Add gold highlights and effects BEFORE adding text
    # Gold gradient overlay
    gold_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    gold_draw = ImageDraw.Draw(gold_overlay)
    
    
    # Add subtle gold sparkles (reduced opacity and size)
    for _ in range(15):  # Reduced from 20 to 15
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)  # Reduced from 2-5 to 1-3
        gold_draw.ellipse([(x, y), (x + size, y + size)], fill=(255, 215, 0, 100))  # Reduced from 150 to 100
    
    # Composite the gold effects onto the main image
    img = Image.alpha_composite(img, gold_overlay)
    
    draw = ImageDraw.Draw(img)
    
    # Get fonts
    fonts = get_fonts()
    
    # Pokemon name and HP
    draw.text((50, 40), pokemon["name"].upper(), font=fonts['name'], fill="black")
    
    # HP bar in top right for non-shiny cards
    max_hp = 200
    hp_percentage = min(pokemon['hp'] / max_hp, 1.0)
    hp_bar_width = 200
    hp_bar_height = 25
    hp_bar_x = width - hp_bar_width - 50
    hp_bar_y = 50
    
    # Draw HP text
    hp_text = f"HP {pokemon['hp']}"
    hp_text_font = ImageFont.truetype(TEXT_FONT, 16)
    hp_text_width = hp_text_font.getlength(hp_text)
    draw.text(
        (hp_bar_x + (hp_bar_width - hp_text_width) // 2, hp_bar_y - 20),
        hp_text,
        font=hp_text_font,
        fill="#FF0000"
    )
    
    # Draw HP bar background
    draw.rectangle(
        [(hp_bar_x, hp_bar_y), (hp_bar_x + hp_bar_width, hp_bar_y + hp_bar_height)],
        fill="#FFB7B7",  # Light red background
        outline="black",
        width=2
    )
    
    # Draw HP bar fill
    draw.rectangle(
        [(hp_bar_x, hp_bar_y), (hp_bar_x + int(hp_bar_width * hp_percentage), hp_bar_y + hp_bar_height)],
        fill="#FF0000",  # Red fill
        outline="black",
        width=2
    )
    
    # Pokemon image
    pokemon_img = get_pokemon_image(pokemon["name"])
    if pokemon_img:
        pokemon_img = pokemon_img.convert('RGBA')
        pokemon_size = (400, 400)
        pokemon_img = pokemon_img.resize(pokemon_size)
        
        # Add a subtle shadow effect
        shadow = Image.new('RGBA', pokemon_img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse([0, pokemon_size[1] - 20, pokemon_size[0], pokemon_size[1]], fill=(0, 0, 0, 100))
        
        # Calculate center position
        img_x = (width - pokemon_size[0]) // 2
        img_y = 150  # Increased from 100 to move image down
        
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
        fill=TYPE_COLORS[pokemon["type"].lower()][0]
    )
    
    # Stats bar with proper font
    stats_y = 560
    draw.text((50, stats_y), f"Attack:  {pokemon['attack']}", font=fonts['stats'], fill="black")
    draw.text((50, stats_y + 30), f"Defense: {pokemon['defense']}", font=fonts['stats'], fill="black")
    
    # Attacks
    attack_y = 650  # Define attack_y before using it
    for attack in pokemon['attacks']:
        # Larger attack background
        attack_height = 100
        draw.rectangle(
            [(40, attack_y), (width - 40, attack_y + attack_height)],
            fill=TYPE_COLORS[pokemon["type"].lower()][1],
            outline=TYPE_COLORS[pokemon["type"].lower()][0],
            width=2
        )
        
        # Attack name
        draw.text((60, attack_y + 20), attack['name'], font=fonts['attack_name'], fill="black")
        
        # Attack damage
        damage_text = f"{attack['damage']}"
        damage_width = fonts['attack_damage'].getlength(damage_text)
        draw.text((width - damage_width - 60, attack_y + 20), damage_text, font=fonts['attack_damage'], fill="black")
        
        attack_y += attack_height + 20
    
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
    
    # Add description text at the bottom
    draw = ImageDraw.Draw(img)
    description = f'"{pokemon["text"]}"'  # Add quotes around the entire text
    description_font = ImageFont.truetype(TEXT_FONT, 24)  # Increased font size
    
    # Calculate maximum width for text (accounting for card borders)
    max_width = width - 100  # Leave 50px margin on each side
    
    # Split text into two lines
    words = description.split()
    mid_point = len(words) // 2
    line1 = ' '.join(words[:mid_point])  # First line with opening quote
    line2 = ' '.join(words[mid_point:])  # Second line with closing quote
    
    # Calculate positions for both lines
    line1_width = description_font.getlength(line1)
    line2_width = description_font.getlength(line2)
    
    # Center both lines
    line1_x = (width - line1_width) // 2
    line2_x = (width - line2_width) // 2
    
    # Position lines with proper spacing
    line_spacing = 10
    text_y = height - 100  # Position from bottom
    
    # Draw both lines
    draw.text((line1_x, text_y), line1, font=description_font, fill="black")
    draw.text((line2_x, text_y + description_font.size + line_spacing), line2, font=description_font, fill="black")
    
    # Convert to RGB for saving
    img = img.convert('RGB')
    
    # Ensure mons directory exists
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)
    
    # Save image in mons directory
    save_path = os.path.join(os.path.dirname(__file__), output_dir, f"{pokemon['name']}_nft.png")
    img.save(save_path, quality=95)
    print(f"NFT card saved as {save_path}")
    return save_path

def create_shining_card(pokemon, output_dir='../../public/mons'):
    # Debug print to verify data
    print(f"Creating shining card for: {pokemon['name']}")
    print(f"Type: {pokemon['type']}")
    print(f"HP: {pokemon['hp']}")
    print(f"Attack: {pokemon['attack']}")
    print(f"Defense: {pokemon['defense']}")
    print(f"Attacks: {pokemon['attacks']}")
    print(f"Text: {pokemon['text']}")
    
    # Pokemon card dimensions (scaled up from standard size)
    width = 750  # 2.5" * 300dpi
    height = 1050  # 3.5" * 300dpi
    
    # Create base image with black background
    img = Image.new("RGBA", (width, height), color="black")
    draw = ImageDraw.Draw(img)
    
    # Add card frame with silver color
    create_card_frame(img, width, height)
    
       # Add gold highlights and effects BEFORE adding text
    # Gold gradient overlay

    
    # Get fonts
    fonts = get_fonts()
    
    # Pokemon name and HP
    draw.text((50, 40), pokemon["name"].upper(), font=fonts['name'], fill="white")
    
    # Move HP bar above attacks and center it
    attack_y = 650
    hp_bar_y = attack_y - 50  # Position HP bar 50 pixels above attacks
    
    # HP bar
    max_hp = 200
    hp_percentage = min(pokemon['hp'] / max_hp, 1.0)
    hp_bar_width = 300  # Increased width for better centering
    hp_bar_height = 25
    hp_bar_x = (width - hp_bar_width) // 2  # Center the bar horizontally
    
    # Draw HP text
    hp_text = f"HP {pokemon['hp']}"
    hp_text_font = ImageFont.truetype(TEXT_FONT, 16)
    hp_text_width = hp_text_font.getlength(hp_text)
    draw.text(
        (hp_bar_x + (hp_bar_width - hp_text_width) // 2, hp_bar_y - 20),
        hp_text,
        font=hp_text_font,
        fill="white"
    )
    
    # Draw HP bar background
    draw.rectangle(
        [(hp_bar_x, hp_bar_y), (hp_bar_x + hp_bar_width, hp_bar_y + hp_bar_height)],
        fill="#333333",
        outline="white",
        width=2
    )
    
    # Draw HP bar fill with silver color
    draw.rectangle(
        [(hp_bar_x, hp_bar_y), (hp_bar_x + int(hp_bar_width * hp_percentage), hp_bar_y + hp_bar_height)],
        fill="#C0C0C0",  # Silver color
        outline="white",
        width=2
    )
    
    # Pokemon image (using shiny artwork)
    pokemon_name = pokemon["name"].replace("Shiny ", "").replace("Shining ", "")
    pokemon_img = get_pokemon_image(pokemon_name, shiny=True)
    if pokemon_img:
        pokemon_img = pokemon_img.convert('RGBA')
        pokemon_size = (400, 400)
        pokemon_img = pokemon_img.resize(pokemon_size)
        
        # Add a subtle shadow effect
        shadow = Image.new('RGBA', pokemon_img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse([0, pokemon_size[1] - 20, pokemon_size[0], pokemon_size[1]], fill=(255, 255, 255, 50))
        
        # Calculate center position - moved down
        img_x = (width - pokemon_size[0]) // 2
        img_y = 150  # Increased from 100 to move down
        
        # Paste shadow and image
        img.paste(shadow, (img_x, img_y), shadow)
        img.paste(pokemon_img, (img_x, img_y), pokemon_img)
        
        # Add gold circle around artwork
        circle_radius = pokemon_size[0] // 2 + 10
        circle_center_x = img_x + pokemon_size[0] // 2
        circle_center_y = img_y + pokemon_size[1] // 2
        
    
    # Attacks
    for attack in pokemon['attacks']:
        attack_height = 100
        draw.rectangle(
            [(40, attack_y), (width - 40, attack_y + attack_height)],
            fill="#333333",
            outline="white",
            width=2
        )
        
        # Attack name
        draw.text((60, attack_y + 20), attack['name'], font=fonts['attack_name'], fill="white")
        
        # Attack damage
        damage_text = f"{attack['damage']}"
        damage_width = fonts['attack_damage'].getlength(damage_text)
        draw.text((width - damage_width - 60, attack_y + 20), damage_text, font=fonts['attack_damage'], fill="white")
        
        attack_y += attack_height + 20
    
    # Add description text at the bottom
    description = f'"{pokemon["text"]}"'
    description_font = ImageFont.truetype(TEXT_FONT, 24)
    
    # Split text into two lines
    words = description.split()
    mid_point = len(words) // 2
    line1 = ' '.join(words[:mid_point])
    line2 = ' '.join(words[mid_point:])
    
    # Calculate positions for both lines
    line1_width = description_font.getlength(line1)
    line2_width = description_font.getlength(line2)
    
    # Center both lines
    line1_x = (width - line1_width) // 2
    line2_x = (width - line2_width) // 2
    
    # Position lines with proper spacing
    line_spacing = 10
    text_y = height - 100
    
    # Draw both lines
    draw.text((line1_x, text_y), line1, font=description_font, fill="white")
    draw.text((line2_x, text_y + description_font.size + line_spacing), line2, font=description_font, fill="white")
    
    gold_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    gold_draw = ImageDraw.Draw(gold_overlay)
    
    # Add subtle gold gradient from top to bottom (reduced opacity)
    for y in range(height):
        alpha = int(35 * (1 - y/height))  # Reduced from 30 to 20
        gold_draw.line([(0, y), (width, y)], fill=(255, 215, 0, alpha))
    

    
    # Add subtle gold sparkles (reduced opacity and size)
    for _ in range(20):  # Reduced from 20 to 15
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(2, 4)  # Reduced from 2-5 to 1-3
        gold_draw.ellipse([(x, y), (x + size, y + size)], fill=(255, 215, 0, 100))  # Reduced from 150 to 100
    
    # Composite the gold effects onto the main image
    img = Image.alpha_composite(img, gold_overlay)
    
    # Convert to RGB for saving
    img = img.convert('RGB')
    
    # Ensure mons directory exists
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)
    
    # Save image in mons directory
    save_path = os.path.join(os.path.dirname(__file__), output_dir, f"{pokemon['name']}_nft.png")
    img.save(save_path, quality=95)
    print(f"Shining NFT card saved as {save_path}")
    return save_path


