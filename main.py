import argparse
import mouse
import multiprocessing
import re
from requests import get
from time import sleep
try: import ujson as json
except ImportError: import json

from os import get_terminal_size, mkdir
from os.path import exists

if __name__ != '__main__' and __name__ != '__mp_main__':
    raise ImportError("This file cannot be imported.")

parser = argparse.ArgumentParser(description='A bot to run macros for Bloons TD6')
parser.add_argument('--debug', action='store_true', help='Enable debug log mode')
parser.add_argument('--restart', action='store_true', help='Restart the macro after every game', default=True)
parser.add_argument('--hijack', action='store_true', help='Allow the program to "steal" control of your mouse', default=True)
parser.add_argument('--path', type=str, help='Folder to load the macro from', required=True)
args = parser.parse_args()

json.dump({
    'debug': args.debug
}, open('config.json', 'w'))

# oh boy i sure love separated imports! i too enjoy violating pep8 standards! (cries in non-pythonic code)
from src.bot import Bot
from src.bloons import is_game_focused
import src.logger as logger

def bot(queue: multiprocessing.Queue):
    bot = Bot('macros/Infernal_Deflation', restart=args.restart, queue=queue, hijack=args.hijack)
    if not is_game_focused():
        logger.info("Waiting for game to be focused... Please switch to the BloonsTD6 window.")
        while not is_game_focused():
            pass
    bot.start()

def check_for_updates() -> bool | None:
    if not exists('.git') or not exists('.git/FETCH_HEAD'): return None
    with open('.git/FETCH_HEAD', 'r') as fp:
        fetch_head = fp.read()
    match = re.match(r"(?P<hash>[0-9a-f]{40}).?+branch '(?P<branch>.*)'", fetch_head)
    if match is None: return None
    hash = match.group('hash')
    branch = match.group('branch')
    r = get(f"https://api.github.com/repos/howlagon/banana_farmer/commits/{branch}")
    if r.status_code != 200: return None
    data = r.json()
    sha = data.get('sha')
    if sha is None: return None
    if sha == hash: return False
    return True

def main():
    queue: multiprocessing.Queue = multiprocessing.Queue()
    bot_thread = multiprocessing.Process(target=bot, args=(queue,), daemon=True)
    bot_thread.start()
    try:
        while mouse.get_position() != (0,0) and bot_thread.is_alive():
            sleep(0.1)
        if bot_thread.is_alive():
            logger.error("Failsafe triggered!")
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        logger.info("Exiting...")
        result = []
        queue.put(None)
        bot_thread.terminate()
    for i in iter(queue.get, None):
        result.append(i)
    if len(result) == 0:
        return
    data = result[-1]

    current_stats = json.load(open('stats.json', 'r'))
    data['monkey_money_earned'] += current_stats['monkey_money_earned']
    data['total_time'] += current_stats['total_time']
    data['games_completed'] += current_stats['games_completed']
    try:
        average_time = (data['total_time'] + (current_stats['average_time'] if current_stats['average_time'] != 0 else 0)) / (data['games_completed'] + (1 if current_stats['average_time'] != 0 else 0))
    except ZeroDivisionError:
        average_time = 0

    stats = {
        'monkey_money_earned': data['monkey_money_earned'],
        'total_time': data['total_time'],
        'games_completed': data['games_completed'],
        'average_time': average_time
    }
    json.dump(stats, open('stats.json', 'w'), indent=4)
    logger.info("Saved stats to stats.json")

if __name__ == "__main__": # because __mp_main__ is a fucking bitch
    width = get_terminal_size().columns
    if width >= 126:
        print("""
 /$$$$$$$                                                         /$$$$$$$$                                                  
| $$__  $$                                                       | $$_____/                                                  
| $$  \ $$ /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$       | $$    /$$$$$$   /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$ 
| $$$$$$$ |____  $$| $$__  $$ |____  $$| $$__  $$ |____  $$      | $$$$$|____  $$ /$$__  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$
| $$__  $$ /$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$  /$$$$$$$      | $$__/ /$$$$$$$| $$  \__/| $$ \ $$ \ $$| $$$$$$$$| $$  \__/
| $$  \ $$/$$__  $$| $$  | $$ /$$__  $$| $$  | $$ /$$__  $$      | $$   /$$__  $$| $$      | $$ | $$ | $$| $$_____/| $$      
| $$$$$$$/  $$$$$$$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$      | $$  |  $$$$$$$| $$      | $$ | $$ | $$|  $$$$$$$| $$      
|_______/ \_______/|__/  |__/ \_______/|__/  |__/ \_______/      |__/   \_______/|__/      |__/ |__/ |__/ \_______/|__/      
    """.lstrip('\n'))
    elif width >= 75:
        print("""
 ____                                  ______                             
|  _ \                                |  ____|                            
| |_) | __ _ _ __   __ _ _ __   __ _  | |__ __ _ _ __ _ __ ___   ___ _ __ 
|  _ < / _` | '_ \ / _` | '_ \ / _` | |  __/ _` | '__| '_ ` _ \ / _ \ '__|
| |_) | (_| | | | | (_| | | | | (_| | | | | (_| | |  | | | | | |  __/ |   
|____/ \__,_|_| |_|\__,_|_| |_|\__,_| |_|  \__,_|_|  |_| |_| |_|\___|_|   
    """.lstrip('\n'))
    elif width >= 60:
        print("""
 ___                             ___                       
| _ ) __ _ _ _  __ _ _ _  __ _  | __|_ _ _ _ _ __  ___ _ _ 
| _ \/ _` | ' \/ _` | ' \/ _` | | _/ _` | '_| '  \/ -_) '_|
|___/\__,_|_||_\__,_|_||_\__,_| |_|\__,_|_| |_|_|_\___|_|  """.lstrip('\n'))
    else:
        print("Banana Farmer")
        print("Wow your terminal is small! Everyone bully the guy with the small terminal!")
    if check_for_updates() is True:
        print("[36mThere is an update available![0m Please update by running [33;1mgit pull[0m in the bot's directory, or by downloading the latest .ZIP from https://github.com/howlagon/banana_farmer")
    # first time setup
    if not exists('stats.json'):
        print("Doing first time setup...")
        json.dump({
            'monkey_money_earned': 0,
            'total_time': 0,
            'games_completed': 0,
            'average_time': 0,
        }, open('stats.json', 'x'), indent=4)
    if not exists('config.json'):
        json.dump({
            'debug': False
        }, open('config.json', 'x'), indent=4)
    if not exists('debug'):
        mkdir('debug')

    if not exists(f'{args.path}/setup.json') and not exists(f'{args.path}/instructions.json'):
        logger.critical(f"Could not find macro at {args.path}!")
        exit(1)
    setup = json.load(open(f'{args.path}/setup.json', 'r')) # this loads setup (1/2). yes this code is terrible i KNOW
    s = f"Using macro from {args.path}"
    print(s)
    print('-'*len(s))
    print(f"Hero: {setup.get('HERO')}")
    print(f"Map: {setup.get('MAP')}")
    print(f"Difficulty: {setup.get('DIFFICULTY')}")
    print(f"Mode: {setup.get('MODE')}")
    print("\nTo quit, press Ctrl+C in the terminal, or move your mouse to the top left corner of your screen.")
    del s
    main()