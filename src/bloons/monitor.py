from tkinter import Tk
from sys import platform, exit

import logger

screen_size = None
def get_screen_size() -> tuple[int, int]:
    global screen_size
    if screen_size is not None:
        return screen_size
    try:
        if platform == "win32":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(2)
        tk = Tk()
        width, height = tk.winfo_screenwidth(), tk.winfo_screenheight()
        screen_size = (width, height)
        return width, height
    except Exception as e:
        logger.critical(f"Could not retrieve monitor resolution!\n{e}")
        exit(1)
