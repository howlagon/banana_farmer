import colorama
from time import strftime

initalized = False
debug_mode = False

def init(debug = False) -> None:
    global initalized, debug_mode
    colorama.init()
    initalized = True
    debug_mode = debug


def log(level: int, message: str, flush: bool = False) -> None:
    if flush:
        suffix = f"\x1b[2K\r"
    else:
        suffix = "\n"
    if level == -1 and debug_mode:
        print(f"{colorama.Fore.CYAN}{strftime('%H:%M:%S')} | [DEBUG] {message}{colorama.Style.RESET_ALL}", end=suffix)
    if level == 0:
        print(f"{colorama.Fore.WHITE}{strftime('%H:%M:%S')} | [INFO] {message}{colorama.Style.RESET_ALL}", end=suffix)
    elif level == 1:
        print(f"{colorama.Fore.YELLOW}{strftime('%H:%M:%S')} | [WARN] {message}{colorama.Style.RESET_ALL}", end=suffix)
    elif level == 2:
        print(f"{colorama.Fore.RED}{strftime('%H:%M:%S')} | [ERROR] {message}{colorama.Style.RESET_ALL}", end=suffix)
    elif level == 3:
        print(f"{colorama.Fore.RED}{strftime('%H:%M:%S')} | [CRITICAL] {message}{colorama.Style.RESET_ALL}", end=suffix)
    else:
        print(f"{colorama.Fore.RED}{strftime('%H:%M:%S')} | [UNKNOWN] {message}{colorama.Style.RESET_ALL}", end=suffix)

def debug(message: str, flush: bool = False) -> None:
    log(-1, message, flush)

def info(message: str, flush: bool = False) -> None:
    log(0, message, flush)

def warn(message: str, flush: bool = False) -> None:
    log(1, message, flush)

def error(message: str, flush: bool = False) -> None:
    log(2, message, flush)

def critical(message: str, flush: bool = False) -> None:
    log(3, message, flush)