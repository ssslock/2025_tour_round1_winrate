from collections import Counter
import re

def normalize_name(name):
    """
    Normalizes item names to a consistent format for comparison.
    Handles prefixes (EA-, MA-, LA-) and specific name variations/typos.
    """
    # Standardize prefixes to full words
    name = name.replace("LA-", "Late-")
    name = name.replace("MA-", "Middle-")
    name = name.replace("EA-", "Early-")

    # Handle specific name variations or known typos from both lists
    # name = name.replace("TNN", "TNN") # For Early-TNN
    # name = name.replace("Abysia", "Abysia") # Common typo for Abysia
    # name = name.replace("Eriu", "Eriu")     # Common typo for Eriu
    # name = name.replace("Ragha", "Ragha")   # For Late-Ragha
    # name = name.replace("Andromania", "Andromania") # Your confirmed typo correction

    # Trim any leftover whitespace
    return name.strip()

def parse_winner_data(item_list_string):
    """
    Counts the occurrences of each winner from a newline-separated string.
    Normalizes names and returns a Counter object.
    """
    items = [normalize_name(item.strip()) for item in item_list_string.strip().split('\n') if item.strip()]
    return Counter(items)

def parse_participator_data(data_string):
    """
    Parses participator data from a string, normalizing names and
    returning a dictionary of participator counts.
    """
    participator_counts = {}
    lines = data_string.strip().split('\n')
    for line in lines:
        if not line.strip(): # Skip empty lines
            continue
        # Use regex to reliably split the name from the number
        match = re.match(r'(.+?)\s+(\d+)$', line.strip())
        if match:
            raw_name = match.group(1).strip()
            count = int(match.group(2))
            normalized_name = normalize_name(raw_name)
            participator_counts[normalized_name] = count
    return participator_counts

def calculate_win_rates(winner_counts, participator_counts):
    """
    Calculates win rates for each item based on winner and participator counts.
    Returns a list of dictionaries, sorted first by era (Early, Middle, Late)
    then by win rate in descending order.
    """
    win_rates = []
    for item_name, wins in winner_counts.items():
        participations = participator_counts.get(item_name, 0) # Get participations, default to 0 if not found

        win_rate = 0.0
        status = "Calculated"
        if participations > 0:
            win_rate = (wins / participations) * 100
        else:
            status = "No participations recorded"
            if wins > 0:
                status = "Winner(s) but no participations recorded"

        win_rates.append({
            "item": item_name,
            "wins": wins,
            "participations": participations,
            "win_rate": win_rate,
            "status": status
        })

    # Define the custom order for prefixes (Eras)
    prefix_sort_order = {
        "Early": 1,
        "Middle": 2,
        "Late": 3
    }

    # Sort results first by prefix order, then by win_rate (descending), then by item name
    sorted_win_rates = sorted(win_rates,
                              key=lambda x: (
                                  prefix_sort_order.get(x['item'].split('-')[0], 99), # Get prefix order, default to high for unknown
                                  -x['win_rate'], # Sort win rate descending
                                  x['item'] # Sort item name alphabetically for ties
                              ))

    return sorted_win_rates

# --- Your data ---
winner_data = """
Late-Ulm
Middle-Arcoscephale
Middle-Pythium
Early-Hinnom
Late-Tien Chi
Late-Ulm
Late-Utgard
Middle-Naba
Middle-Man
Late-Ragha
Late-Ulm
Middle-Sceleria
Middle-Ctis
Early-Mekone
Early-Yomi
Middle-Pyrene
Late-Ulm
Middle-Sceleria
Late-Utgard
Late-Pangaea
Late-Man
Early-Muspelheim
Late-Andromania
Early-Yomi
Middle-Machaka
Late-Feminie
Middle-Pythium
Middle-Man
Middle-Jotunheim
Late-Marignon
Late-Ulm
Middle-Machaka
Early-Vanheim
Late-Pyrene
Middle-Nidavangr
Early-Rus
Late-Pythium
Late-Utgard
Late-Utgard
Middle-Naba
Early-Muspelheim
Early-Muspelheim
Late-Piconye
Middle-Phlegra
Early-TNN
Early-Rus
Early-Muspelheim
Early-Yomi
Middle-Jotunheim
Middle-Pythium
Early-Niefelheim
Early-Lanka
Late-Andromania
Early-Mictlan
Early-Rus
Early-Yomi
Middle-Vanarus
Early-Mekone
Middle-Man
Late-Vaettiheim
Early-Vanheim
Late-Pythium
Late-Marignon
Middle-Marignon
Middle-Naba
Early-Pangaea
Late-Ulm
Late-Pythium
Early-Yomi
Middle-Ulm
Early-Vanheim
Late-Pangaea
Late-Ctis
Early-Caelum
Middle-Nidavangr
Late-Pangaea
Early-TNN
Late-Pangaea
Middle-Eriu
Middle-Man
Early-Fomoria
Early-Vanheim
Late-Marignon
Late-Atlantis
Late-Man
Middle-Shinuyama
Middle-Man
Middle-Ulm
Early-Lanka
Late-Andromania
"""

participator_data = """
MA-Man 17
LA-Andromania 16
LA-Utgard 16
LA-Ulm 13
MA-Naba 13
LA-Pangaea 12
EA-Muspelheim 11
EA-Rus 11
LA-Pythium 11
MA-Machaka 11
EA-Mekone 10
EA-Yomi 10
LA-Feminie 10
LA-Gath 10
MA-Marignon 10
LA-Man 9
MA-Pangaea 9
MA-Sceleria 9
EA-Fomoria 8
EA-Abysia 7
EA-Caelum 7
EA-Vanheim 7
LA-Agartha 7
LA-Marignon 7
LA-Ragha 7
MA-Nidavangr 7
MA-Ulm 7
EA-Hinnom 6
EA-Niefelheim 6
EA-TNN 6
LA-Pyrene 6
MA-Ind 6
EA-Ermor 5
EA-Lanka 5
EA-Machaka 5
EA-Pangaea 5
EA-Sauromatia 5
LA-Ctis 5
MA-Ashdod 5
MA-Ctis 5
EA-Agartha 4
EA-Ctis 4
LA-Arcoscephale 4
LA-Atlantis 4
LA-Caelum 4
LA-Patala 4
LA-Piconye 4
MA-Abysia 5
MA-Bandar Log 4
MA-Pyrene 4
MA-Pythium 4
MA-Shinuyama 4
EA-Helheim 3
EA-Mictlan 3
EA-Ulm 3
LA-Tien Chi 3
LA-Vaettiheim 3
MA-Caelum 3
MA-Jotunheim 3
MA-Nazca 3
MA-Vanarus 3
MA-Vanheim 3
EA-Arcoscephale 2
EA-Kailasa 2
EA-Tien Chi 2
LA-Bogarus 2
LA-Jomon 2
LA-Midgard 2
LA-Phlegra 2
MA-Arcoscephale 2
MA-Eriu 3
EA-Berytos 1
EA-Pyrene 1
EA-Xibalba 1
LA-Abysia 1
LA-Xibalba 1
MA-Agartha 1
MA-Mictlan 1
MA-Phlegra 1
MA-Tien Chi 1
MA-Uruk 1
"""

# 1. Parse the winner data
winner_counts = parse_winner_data(winner_data)

# 2. Parse the participator data
participator_counts = parse_participator_data(participator_data)

# 3. Calculate win rates
win_rates = calculate_win_rates(winner_counts, participator_counts)

# 4. Print the results
print("--- Win Rates (Sorted by Win Rate) ---")
print(f"{'Item':<25} | {'Wins':>5} | {'Participations':>14} | {'Win Rate (%)':>12} | Status")
print("-" * 75)

for result in win_rates:
    item = result['item']
    wins = result['wins']
    participations = result['participations']
    win_rate = result['win_rate']
    status = result['status']

    if status == "Calculated":
        print(f"{item:<25} | {wins:>5} | {participations:>14} | {win_rate:>11.2f}% | {status}")
    else:
        print(f"{item:<25} | {wins:>5} | {participations:>14} | {'N/A':>11}    | {status}")

# Optionally, list items that participated but never won
print("\n--- Items that Participated but Never Won ---")
participated_but_no_wins = []
for item_name, participations in participator_counts.items():
    if item_name not in winner_counts and participations > 0:
        participated_but_no_wins.append(f"{item_name}: {participations} participations")

if participated_but_no_wins:
    for entry in sorted(participated_but_no_wins): # Sort alphabetically for consistent output
        print(f"- {entry}")
else:
    print("No items found that participated but never won from the provided data.")

print("\n--- Items that Won but Had No Recorded Participations ---")
won_but_no_participations = []
for item_name, wins in winner_counts.items():
    if item_name not in participator_counts:
        won_but_no_participations.append(f"{item_name}: {wins} wins")

if won_but_no_participations:
    for entry in sorted(won_but_no_participations): # Sort alphabetically
        print(f"- {entry}")
else:
    print("No items found that won but had no recorded participations from the provided data.")