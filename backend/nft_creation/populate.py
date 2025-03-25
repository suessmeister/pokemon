from artwork import create_nft_card
import glob
import os

# clear the mons directory
# mons is located in ../../mons

os.makedirs('../../mons', exist_ok=True)
files = glob.glob('../../mons.*')
for f in files:
    os.remove(f)


create_nft_card("Charizard", "fire", 100, 90, 100, [("Fire Punch", 50), ("Flame Charge", 40)])
create_nft_card("Blastoise", "water", 120, 100, 120, [("Hydro Pump", 80), ("Water Gun", 60)])
create_nft_card("Venusaur", "grass", 110, 100, 110, [("Razor Leaf", 70), ("Solar Beam", 90)])
create_nft_card("Pikachu", "electric", 110, 90, 110, [("Thunderbolt", 80), ("Quick Attack", 60)])
create_nft_card("Gengar", "ghost", 120, 100, 120, [("Shadow Ball", 80), ("Night Shade", 70)])
create_nft_card("Mewtwo", "psychic", 130, 110, 130, [("Psystrike", 90), ("Shadow Punch", 80)])
create_nft_card("Nidoking", "poison", 100, 130, 100, [("Toxic", 50), ("Poison Jab", 40)])
create_nft_card("Nidoqueen", "poison", 100, 130, 100, [("Toxic", 50), ("Poison Jab", 40)])
