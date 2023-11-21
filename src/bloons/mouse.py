import pyautogui
from time import sleep

import src.bloons.data as data
from .game import find_current_screen

def block() -> None:
    sleep(0.5)

def _click(x: int, y: int, button: str = "left", duration: float = 0.1) -> None:
    pyautogui.click(x, y, button=button, duration=duration)

def click_map_difficulty(difficulty: str) -> None:
    match difficulty.upper():
        case "BEGINNER":
            _click(580, 980)
        case "INTERMEDIATE":
            _click(835, 980)
        case "ADVANCED":
            _click(1090, 980)
        case 'EXPERT':
            _click(1340, 980)
        case _:
            raise ValueError(f"Invalid difficulty: {difficulty}")

def click_map():
    pass

def navigate_map_picker(direction: str) -> None:
    match direction:
        case 'left':
            _click(275, 430)
        case 'right':
            _click(1645, 430)
        case _:
            raise ValueError(f"Invalid direction: {direction}")

def navigate_home(screen: str | None = None) -> None:
    screen = screen if screen is not None else find_current_screen()
    assert screen in ['map_picker', 'settings']
    if screen in ['map_picker', 'settings']:
        _click(80, 55)
        _click(80, 215)
    block()

def navigate_to_map(map_name: str) -> None:
    if find_current_screen() != 'map_picker': navigate_home()
    map_name = map_name.upper()
    if map_name not in data.maps:
        raise ValueError(f"Invalid map name: {map_name}")
    map_data = data.maps[map_name]
    match data.get_map_difficulty(map_data[0]):
        case 'BEGINNER':
            click_map_difficulty('INTERMEDIATE')
        case _:
            click_map_difficulty('BEGINNER')
    click_map_difficulty(data.get_map_difficulty(map_data[0]))
    for _ in range(map_data[0] - data.map_pages[data.get_map_difficulty(map_data[0])]):
        navigate_map_picker('right')

def navigate_to_settings() -> None:
    assert find_current_screen() == 'home_screen'
    _click(80, 215)
    block()

def navigate_to_map_picker() -> None:
    assert find_current_screen() == 'home_screen'
    _click(840, 940)
    block()