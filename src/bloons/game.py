import re
from ctypes import wintypes, windll, create_unicode_buffer

import src.bloons.data as data
import src.bloons.image as image
import src.logger as logger
from src.utils import block
from src.bloons.keyboard import press_key

current_version = None

def find_current_screen():
    screenshot = image.screenshot()
    images = [
        'assets/screens/home_screen.png',
        'assets/screens/map_picker.png',
        'assets/screens/settings.png',
        'assets/screens/restart.png',
        'assets/screens/level_up.png',
        'assets/screens/monkey_knowledge.png',
        'assets/screens/in_game.png',
        'assets/screens/difficulty_picker.png',
        'assets/screens/map_mode_picker.png',
        'assets/screens/pause_menu.png',
    ]
    match image.find_many_images(images, screenshot):
        case 0: return 'home_screen'
        case 1: return 'map_picker'
        case 2: return 'settings'
        case 3: return 'restart'
        case 4: return 'level_up'
        case 5: return 'monkey_knowledge'
        case 6: return 'in_game'
        case 7: return 'difficulty_picker'
        case 8: return 'map_mode_picker'
        case 9: return 'pause_menu'
        case -1:
            return ''

from src.bloons.mouse import navigate_home, navigate_to_settings, _click

def find_monkey_money() -> int | None:
    if find_current_screen() != 'home_screen': navigate_home()
    image_left = image.find_image(image_path='assets/monkey_money_left.png')
    if image_left is None: return None
    image_right = image.find_image(image_path='assets/monkey_money_right.png')
    if image_right is None: return None
    width = image_right[0] - image_left[0] - image_left[2] - 25
    left = image_left[0] + image_left[2] + 20

    screenshot = image.screenshot(bounds=[int(left), 30, int(width), 60])
    text = image.ocr(screenshot, threshold=(150, 255), invert = True).replace(',', '').replace(' ', '').replace('\n', '')
    if text.isdigit():
        return int(text)
    logger.error(f"Could not find monkey money! Found: {text}")
    return None

def find_current_version() -> str:
    global current_version
    if current_version is not None:
        return current_version
    for _ in range(2):
        if find_current_screen() != 'settings': navigate_to_settings()
        else: break
    if find_current_screen() != 'settings':
        logger.critical("Could not navigate to settings!")
        exit(1)
    screenshot = image.screenshot(bounds=[620, 1020, 650, 36])
    text = image.ocr(screenshot, threshold=(150, 255), invert = True)
    text = text.replace('\n', '')
    match = re.search(r'Version ([0-9\.]+)', text)
    if match is not None:
        current_version = match.group(1)
        return current_version
    logger.error(f"Could not find version! Found: \"{text}\"")

def find_current_round() -> int | None:
    if find_current_screen() != 'in_game':
        logger.error("Not in game!")
        return None
    screenshot = image.screenshot(bounds=[1400, 30, 160, 40])
    text = image.ocr(screenshot, threshold=(250, 255), invert = True).replace("\n", '\\n')
    match = re.search(r'([0-9]+)', text)
    if match is not None:
        if not match.group(1).isdigit(): return None
        return int(match.group(1))
    if text != 'rs\\n': # gray overlay, likely a popup window
        logger.error(f"Could not find round! Found: \"{text}\"")
    return None

def is_game_focused() -> bool:
    # https://stackoverflow.com/a/58355052/16126645
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    return buf.value == 'BloonsTD6'

autostart_state = None
def is_auto_start_enabled() -> bool | None:
    global autostart_state
    if autostart_state is not None:
        return autostart_state
    screen = find_current_screen()
    if screen != 'pause_menu':
        if screen != 'in_game':
            logger.error("Not in game!")
            return None
        press_key(data.Hotkeys.pause)
        block()
    screenshot = image.screenshot()
    pixel = image.get_pixel(screenshot, (1325, 305))
    autostart_state = pixel[1] >= 200
    return autostart_state

def toggle_autostart(state: bool) -> None:
    if is_auto_start_enabled() != state:
        _click(1325, 305)
    press_key('esc')

def start_game(fast_forward: bool = True) -> None:
    if find_current_screen() != 'in_game':
        logger.error("Not in game!")
        return
    press_key(data.Hotkeys.play)
    if fast_forward:
        press_key(data.Hotkeys.play)