from src.bloons import is_game_focused, find_current_screen, select_map, toggle_autostart, start_game
from src.bloons.monkey import place_monkey, upgrade_monkey

while not is_game_focused():
    pass
if find_current_screen() != 'in_game': 
    select_map('monkey meadow', 'easy', 'standard')
while not find_current_screen() == 'in_game':
    pass
toggle_autostart(True)
place_monkey('DART', (619, 494))
upgrade_monkey((619, 494), [0, 2, 2])
start_game()