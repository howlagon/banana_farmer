import keyboard
from time import sleep

def press_key(key: str, duration: float = 0.1, delay: float = 0.05) -> None:
    """A (blocking!) function to press a certain key for a set duration

    Args:
        key (str)
        duration (float, optional). Defaults to 0.1.
        delay (float, optional). Defaults to 0.05. The delay after pressing the key
    """
    if key == 'esc': key = 'escape'
    keyboard.press(key)
    sleep(duration)
    keyboard.release(key)
    sleep(delay)