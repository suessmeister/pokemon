from artwork import create_nft_card, create_shining_card
import glob
import os
import json
import shutil

# Load Pokemon data from shared JSON file
with open(os.path.join(os.path.dirname(__file__), '../../src/data/pokemon.json'), 'r') as f:
    pokemon_data = json.load(f)

# Load Shining Pokemon data
with open(os.path.join(os.path.dirname(__file__), '../../src/data/shining.json'), 'r') as f:
    shining_data = json.load(f)

# Create directories if they don't exist
regular_dir = os.path.join(os.path.dirname(__file__), '../../public/mons')
shiny_dir = os.path.join(os.path.dirname(__file__), '../../public/mons/shiny')
os.makedirs(regular_dir, exist_ok=True)
os.makedirs(shiny_dir, exist_ok=True)

# Clear existing files in both directories
def clear_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)

# Clear both directories
clear_directory(regular_dir)
clear_directory(shiny_dir)

# Create NFT cards for each Pokemon
print("\nGenerating Pokemon cards...")
for pokemon in pokemon_data['pokemon']:
    create_nft_card(
        pokemon,
        output_dir='../../public/mons'
    )

# Create Shining Pokemon cards
print("\nGenerating Shining Pokemon cards...")
for pokemon in shining_data['shining']:
    if pokemon and 'name' in pokemon:  # Check if pokemon exists and has a name
        create_shining_card(
            pokemon,
            output_dir='../../public/mons/shiny'
        )

print("\nPokemon cards generated successfully!")
print(f"Regular cards saved in: {regular_dir}")
print(f"Shining cards saved in: {shiny_dir}")


