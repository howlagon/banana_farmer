import mouse
from time import sleep

import src.bloons.data as data
import src.bloons.image as image
from src.bloons.game import find_current_screen
import src.logger as logger
from src.utils import block

def _click(x: int, y: int, button: str = "left", duration: float = 0.15) -> None:
    mouse.move(x, y, duration=0.1)
    mouse.press(button=button)
    sleep(duration)
    mouse.release(button=button)

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

def navigate_to_settings() -> None:
    assert find_current_screen() == 'home_screen'
    _click(80, 215)
    block()

def navigate_to_map_picker() -> None:
    assert find_current_screen() == 'home_screen'
    _click(840, 940)
    block()

def navigate_to_map(map_name: str) -> None:
    if find_current_screen() != 'map_picker': navigate_to_map_picker()
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
    match map_data[1]:
        case 0: _click(540, 265)
        case 1: _click(965, 265)
        case 2: _click(1390, 265)
        case 3: _click(540, 580)
        case 4: _click(965, 580)
        case 5: _click(1390, 580)
    block()

def select_difficulty(difficulty: str) -> None:
    screen = find_current_screen()
    if screen != 'difficulty_picker':
        logger.warn(f'Current screen may not be difficulty picker! Found: {screen}')
    match difficulty.upper():
        case 'EASY': _click(635, 405)
        case 'MEDIUM': _click(965, 405)
        case 'HARD': _click(1295, 405)
    block()

def select_map_mode(difficulty: str, mode: str) -> None:
    select_difficulty(difficulty)
    screen = find_current_screen()
    if screen != 'map_mode_picker':
        logger.warn(f'Current screen may not be mode picker! Found: {screen}')
    match difficulty.upper():
        case 'EASY':
            match mode.upper():
                case 'STANDARD': _click(640, 595)
                case 'PRIMARY ONLY': _click(960, 455)
                case 'DEFLATION': _click(1285, 455)
                case 'SANDBOX': _click(960, 740)
        case _:
            raise NotImplementedError(f"Difficulty {difficulty} not implemented yet!")

def select_map(map: str, difficulty: str, mode: str) -> None:
    navigate_to_map(map)
    select_map_mode(difficulty, mode)
    block()
    if image.find_image(image_path='assets/screens/overwrite_save.png') is not None:
        _click(1140, 730)
    block()