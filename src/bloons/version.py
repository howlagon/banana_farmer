import re

from src.bloons.game import find_current_version
import src.bloons.logger as logger

minor_version = '39.2'
major_version = minor_version[:minor_version.rfind('.')]

def check_version_number(version: str | None = None) -> bool:
    """Checks if the program version matches the game version.

    Returns:
        bool
    """
    game_version = version if version is not None else re.search(r'([0-9]+?)', find_current_version()).group(1)
    return game_version == major_version

def check_minor_version(version: str | None = None) -> bool:
    """Checks if the program version matches the game version.

    Returns:
        bool
    """
    game_version = version if version is not None else  re.search(r'([0-9]+?\.[0-9]+?)', find_current_version()).group(1)
    return game_version == minor_version

def check_version() -> None:
    logger.info("Checking version number...", flush=True)
    if check_version_number(): return
    game_version = re.search(r'([0-9]+?\.[0-9]+?)', find_current_version()).group(1)
    if not check_version_number(game_version.split('.')[0]):
        logger.warn(f"Version number mismatch! Program version: {minor_version}, Game version: {game_version}")
        print("Would you like to continue? This may negatively affect the program! (y/n default: n) ", end='')
        if input().lower() != 'y':
            exit(0)
        return
    if not check_minor_version(game_version):
        logger.warn(f"Version number mismatch! Program version: {minor_version}, Game version: {game_version}")
        print("Would you like to continue? This likely will have no affect, although may. (y/n default: y) ", end='')
        user_input = input().lower()
        if user_input == 'n':
            exit(0)
        elif user_input != 'y' and user_input != '':
            logger.warn("Invalid input! Continuing...")