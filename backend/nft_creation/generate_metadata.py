import json
import os
from datetime import datetime

def generate_metadata(pokemon, is_shining=False):
    """Generate Metaplex metadata for a Pokemon card"""
    # Base metadata structure
    metadata = {
        "name": f"{pokemon['name']} {'Shining' if is_shining else ''} Card",
        "symbol": "POKE",
        "description": pokemon['text'],
        "seller_fee_basis_points": 500,  # 5% royalty
        "image": f"{pokemon['name']}_nft.png",
        "attributes": [
            {
                "trait_type": "Type",
                "value": pokemon['type'].capitalize()
            },
            {
                "trait_type": "HP",
                "value": pokemon['hp']
            },
            {
                "trait_type": "Attack",
                "value": pokemon['attack']
            },
            {
                "trait_type": "Defense",
                "value": pokemon['defense']
            },
            {
                "trait_type": "Rarity",
                "value": "Shining" if is_shining else "Regular"
            }
        ],
        "properties": {
            "files": [
                {
                    "uri": f"{pokemon['name']}_nft.png",
                    "type": "image/png"
                }
            ],
            "category": "image",
            "creators": [
                {
                    "address": "YOUR_CREATOR_ADDRESS",  # Replace with actual creator address
                    "share": 100
                }
            ]
        }
    }

    # Add attack information as attributes
    for i, attack in enumerate(pokemon['attacks'], 1):
        metadata['attributes'].extend([
            {
                "trait_type": f"Attack {i} Name",
                "value": attack['name']
            },
            {
                "trait_type": f"Attack {i} Damage",
                "value": attack['damage']
            }
        ])

    return metadata

def main():
    # Load Pokemon data
    with open(os.path.join(os.path.dirname(__file__), '../../src/data/pokemon.json'), 'r') as f:
        pokemon_data = json.load(f)

    # Load Shining Pokemon data
    with open(os.path.join(os.path.dirname(__file__), '../../src/data/shining.json'), 'r') as f:
        shining_data = json.load(f)

    # Create metadata directories
    metadata_dir = os.path.join(os.path.dirname(__file__), '../../public/metadata')
    shiny_metadata_dir = os.path.join(metadata_dir, 'shiny')
    os.makedirs(metadata_dir, exist_ok=True)
    os.makedirs(shiny_metadata_dir, exist_ok=True)

    # Generate metadata for regular Pokemon
    print("\nGenerating metadata for regular Pokemon...")
    for pokemon in pokemon_data['pokemon']:
        metadata = generate_metadata(pokemon)
        output_path = os.path.join(metadata_dir, f"{pokemon['name']}_metadata.json")
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Generated metadata for {pokemon['name']}")

    # Generate metadata for shining Pokemon
    print("\nGenerating metadata for shining Pokemon...")
    for pokemon in shining_data['shining']:
        if pokemon and 'name' in pokemon:
            metadata = generate_metadata(pokemon, is_shining=True)
            output_path = os.path.join(shiny_metadata_dir, f"{pokemon['name']}_metadata.json")
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Generated metadata for shining {pokemon['name']}")

    print("\nMetadata generation complete!")
    print(f"Regular metadata saved in: {metadata_dir}")
    print(f"Shining metadata saved in: {shiny_metadata_dir}")

if __name__ == "__main__":
    main() 