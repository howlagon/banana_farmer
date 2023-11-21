from time import sleep

from src.bloons.mouse import _click
from src.bloons.keyboard import press_key
import src.bloons.data as data

def select_monkey(type: str) -> None:
    hotkey = data.Hotkeys.monkeys[type]
    press_key(hotkey)

def place_monkey(type: str, position: tuple[int, int]) -> None:
    select_monkey(type)
    x, y = position
    _click(x, y)

def upgrade_monkey(position: tuple[int, int], path: list[int, int, int]) -> None:
    x, y = position
    _click(x, y)
    for i in range(0, 3):
        for _ in range(0, path[i]):
            press_key(data.Hotkeys.upgrades[i])
    press_key('esc')