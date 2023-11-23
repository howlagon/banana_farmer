try: import ujson as json
except ImportError: import json

from src.bloons.mouse import _click
from src.bloons.keyboard import press_key
from src.utils import block
import src.bloons.data as data

def select_monkey(type: str) -> None:
    hotkey = data.Hotkeys.monkeys[type]
    press_key(hotkey)

def place_tower(type: str, position: tuple[int, int]) -> None:
    select_monkey(type)
    x, y = position
    _click(x, y)
    block(0.25)

def upgrade_tower(position: tuple[int, int], path: list[int, int, int]) -> None:
    x, y = position
    _click(x, y)
    block(0.25)
    for i in range(0, 3):
        for _ in range(0, path[i]):
            press_key(data.Hotkeys.upgrades[i], duration=0.1, delay=0.1)
    press_key('esc')
    block(0.25)

def sell_tower(position: tuple[int, int]) -> None:
    x, y = position
    _click(x, y)
    block(0.25)
    press_key(data.Hotkeys.sell)
    block(0.25)

def change_targeting(position: tuple[int, int], current: str, desired: str) -> None:
    _click(position[0], position[1])
    block(0.25)
    order = ['FIRST', 'LAST', 'CLOSE', 'STRONG']
    
    current_index = order.index(current)
    desired_index = order.index(desired)

    if current_index > desired_index:
        for _ in range(current_index - desired_index):
            press_key(data.Hotkeys.change_targeting)
    elif current_index < desired_index:
        for _ in range(desired_index - current_index):
            press_key(data.Hotkeys.change_targeting)
    block(0.25)
    press_key('esc')
    block(0.25)

class Towers:
    def __init__(self) -> None:
        self.towers: dict[tower] = {}
    
    def place_tower(self, type: str, position: tuple[int, int], path: list = [0, 0, 0], target: str = 'FIRST') -> None:
        if json.dumps(position) in self.towers.keys():
            raise ValueError(f"Tower already exists at {position}")
        self.towers[json.dumps(position)] = tower(type, position, path, target)
    
    def upgrade_tower(self, position: tuple[int, int], path: list[int, int, int]) -> None:
        if json.dumps(position) not in self.towers.keys():
            raise ValueError(f"No tower exists at {position}")
        self.towers[json.dumps(position)].upgrade(path)
    
    def sell_tower(self, position: tuple[int, int]) -> None:
        if json.dumps(position) not in self.towers.keys():
            raise ValueError(f"No tower exists at {position}")
        self.towers[json.dumps(position)].sell()
        del self.towers[json.dumps(position)]
        
        
class tower:
    def __init__(self, type: str, position: tuple[int, int], path: list = [0, 0, 0], target: str = 'FIRST') -> None:
        self.position = position
        self.type = type
        self.path = path
        self.target = target
        place_tower(type, position)
        if path != [0, 0, 0]: upgrade_tower(position, path)
        if self.target != 'FIRST': change_targeting(position, 'FIRST', target)
    
    def upgrade(self, path: list[int, int, int]) -> None:
        self.path = path
        upgrade_tower(self.position, path)
    
    def change_targeting(self, targeting: str) -> None:
        self.targeting = targeting
        change_targeting(self.position, self.targeting)
    
    def sell(self) -> None:
        sell_tower(self.position)
        del self