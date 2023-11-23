class Hotkeys:
    monkeys = {
        'DART': 'q',
        'BOOMERANG': 'w',
        'BOMB': 'e',
        'TACK': 'r',
        'ICE': 't',
        'GLUE': 'y',
        'SNIPER': 'z',
        'SUB': 'x',
        'BUCCANEER': 'c',
        'ACE': 'v',
        'HELI': 'b', 'PILOT': 'b',
        'MORTAR': 'n',
        'DARTLING': 'm',
        'WIZARD': 'a',
        'SUPER': 's',
        'NINJA': 'd',
        'ALCHEMIST': 'f',
        'DRUID': 'g',
        'FARM': 'h',
        'ENGINEER': 'l',
        'SPIKE': 'j',
        'VILLAGE': 'k',
        'BEAST': 'i',
        'HERO': 'o'
    }

    upgrades = [
        ',', '.', '/'
    ]
    change_targeting = 'tab'
    reverse_change_targeting = 'ctrl+tab'
    sell = 'backspace'
    play = 'space'
    send_next_round = 'shift+space'
    pause = '`'
    abilities = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='
    ]
    monkey_special = 'pagedown'

# [page, index]
maps = {
    # beginner
    'MONKEY_MEADOW': [0, 0],
    'IN_THE_LOOP': [0, 1],
    'MIDDLE_OF_THE_ROAD': [0, 2],
    'TREE_STUMP': [0, 3],
    'TOWN_CENTER': [0, 4],
    'ONE_TWO_TREE': [0, 5],
    'SCRAPYARD': [1, 0],
    'THE_CABIN': [1, 1],
    'RESORT': [1, 2],
    'SKATES': [1, 3],
    'LOTUS_ISLAND': [1, 4],
    'CANDY_FALLS': [1, 5],
    'WINTER_PARK': [2, 0],
    'CARVED': [2, 1],
    'PARK_PATH': [2, 2],
    'ALPINE_RUN': [2, 3],
    'FROZEN_OVER': [2, 4],
    'CUBISM': [2, 5],
    'FOUR_CIRCLES': [3, 0],
    'HEDGE': [3, 1],
    'END_OF_THE_ROAD': [3, 2],
    'LOGS': [3, 3],
    # intermediate
    'WATER_PARK': [4, 0],
    'POLYPHEMUS': [4, 1],
    'COVERED_GARDEN': [4, 2],
    'QUARRY': [4, 3],
    'QUIET_STREET': [4, 4],
    'BLOONARIUS_PRIME': [4, 5],
    'BALANCE': [5, 0],
    'ENCRYPTED': [5, 1],
    'BAZAAR': [5, 2],
    "ADORA'S_TEMPLE": [5, 3],
    'SPRING_SPRING': [5, 4],
    'KARTSNDARTS': [5, 5],
    'MOON_LANDING': [6, 0],
    'HAUNTED': [6, 1],
    'DOWNSTREAM': [6, 2],
    'FIRING_RANGE': [6, 3],
    'CRACKED': [6, 4],
    'STREAMBED': [6, 5],
    'CHUTES': [7, 0],
    'RAKE': [7, 1],
    'SPICE_ISLANDS': [7, 2],
    # advanced
    'DARK_CASTLE': [8, 0],
    'EROSION': [8, 1],
    'MIDNIGHT_MANSION': [8, 2],
    'SUNKEN_COLUMNS': [8, 3],
    'X_FACTOR': [8, 4],
    'MESA': [8, 5],
    'GEARED': [9, 0],
    'SPILLWAY': [9, 1],
    'CARGO': [9, 2],
    "PAT'S_POND": [9, 3],
    'PENINSULA': [9, 4],
    'HIGH_FINANCE': [9, 5],
    'ANOTHER_BRICK': [10, 0],
    'OFF_THE_COAST': [10, 1],
    'CORNFIELDS': [10, 2],
    'UNDERGROUND': [10, 3],
    # expert
    'DARK_DUNGEONS': [11, 0],
    'SANCTUARY': [11, 1],
    'RAVINE': [11, 2],
    'FLOODED_VALLEY': [11, 3],
    'INFERNAL': [11, 4],
    'BLOODY_PUDDLES': [11, 5],
    'WORKSHOP': [12, 0],
    'QUAD': [12, 1],
    'DARK_CASTLE': [12, 2],
    'MUDDY_PUDDLES': [12, 3],
    '#OUCH': [12, 4],
}
map_pages = {
    'BEGINNER': 0,
    'INTERMEDIATE': 4,
    'ADVANCED': 8,
    'EXPERT': 11
}

# [row, column]
languages = {
    'ENGLISH': [0, 0],
    'GERMAN': [0, 1],
    'FRENCH': [0, 2],
    'SPANISH (SP)': [0, 3],
    'SPANISH (LATAM)': [1, 0],
    'ITALIAN': [1, 1],
    'PORTUGUESE (BR)': [1, 2],
    'NORWEGIAN': [1, 3],
    'SWEDISH': [2, 0],
    'FINNISH': [2, 1],
    'DANISH': [2, 2],
    'DUTCH': [2, 3],
    'RUSSIAN': [3, 0],
    'TURKISH': [3, 1],
    'KOREAN': [3, 2],
    'JAPANESE': [3, 3],
    'CHINESE (SIMPLIFIED)': [4, 0],
    'CHINESE (TRADITIONAL)': [4, 1],
    'POLISH': [4, 2],
    'THAI': [4, 3],
    'MONKISH': [5, 0],
}

def get_map_difficulty(page: int) -> str:
    if page < map_pages['INTERMEDIATE']: return 'BEGINNER'
    if page < map_pages['ADVANCED']: return 'INTERMEDIATE'
    if page < map_pages['EXPERT']: return 'ADVANCED'
    return 'EXPERT'