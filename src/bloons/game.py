import re

import src.bloons.image as image
import src.bloons.logger as logger

current_version = None

def find_current_screen():
    screenshot = image.screenshot()
    images = [
        'assets/screens/home_screen.png',
        'assets/screens/map_picker.png',
        'assets/screens/settings.png',
        'assets/screens/in_game.png',
    ]
    match image.find_many_images(images, screenshot):
        case 0:
            return 'home_screen'
        case 1:
            return 'map_picker'
        case 2:
            return 'settings'
        case 3:
            return 'in_game'
        case -1:
            return ''

from src.bloons.mouse import navigate_home, navigate_to_settings

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