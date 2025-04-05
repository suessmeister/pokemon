from artwork import create_nft_card
import glob
import os
import json
import shutil

# Load Pokemon data from shared JSON file
with open(os.path.join(os.path.dirname(__file__), '../../src/data/pokemon.json'), 'r') as f:
    pokemon_data = json.load(f)

# clear the mons directory
# mons is located in ../../mons
os.makedirs('../../public/mons', exist_ok=True)
files = glob.glob('../../public/mons/*')
for f in files:
    os.remove(f)

# Create NFT cards for each Pokemon
print("\nGenerating Pokemon cards...")
for pokemon in pokemon_data['pokemon']:
    create_nft_card(
        pokemon['name'],
        pokemon['type'],
        pokemon['attack'],
        pokemon['defense'],
        pokemon['hp'],
        [(attack['name'], attack['damage']) for attack in pokemon['attacks']],
    )

print("\nPokemon cards generated successfully in public/mons directory!")
# Copy generated images to public directory
print("\nCopying images to public directory...")
os.makedirs('../../public/mons', exist_ok=True)
for file in glob.glob('../../mons/*'):
    shutil.copy2(file, '../../public/mons/')

