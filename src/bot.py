try: import ujson as json
except ImportError: import json
import traceback
import multiprocessing
from time import time

from src.bloons import Towers, select_map, find_current_round, find_current_screen, start_game, press_key
from src.utils import block
from src.bloons.image import find_image, find_many_images, ocr
from src.bloons.mouse import _click
import src.bloons.data as data
import src.logger as logger

towers = Towers()

def parse_move(move: dict):
    logger.debug(f"Move: {move}")
    match move['INSTRUCTION']:
        case 'START':
            ff = move.get('FAST_FORWARD')
            start_game(ff if ff is not None else True)
        case 'PLACE_TOWER':
            towers.place_tower(move['MONKEY'], move['LOCATION'], move['UPGRADE_PATH'] if move.get('UPGRADE_PATH') is not None else [0, 0, 0], move['TARGET'] if move.get('TARGET') is not None else 'FIRST')
        case 'UPGRADE_TOWER':
            towers.upgrade_tower(move['LOCATION'], move['UPGRADE_PATH'])
        case 'SELL_TOWER':
            towers.sell_tower(move['LOCATION'])
        case 'CHANGE_TARGET':
            towers.change_target(move['LOCATION'], move['TARGET'])

def restart_from_victory_screen() -> None:
    _click(1195, 850)
    block(1)
    _click(960, 760)
    block(1)
    press_key(data.Hotkeys.pause)
    block()
    _click(1075, 840)
    while not find_current_screen() == 'restart':
        pass
    _click(1140, 730)
    block()

images = [
                'assets/screens/victory.png',
                'assets/screens/level_up.png',
                'assets/screens/monkey_knowledge.png',
            ]

stats = {
    'monkey_money_earned': 0,
    'total_time': 0,
    'games_completed': 0,
    'games_won': 0
}

def find_monkey_money_earned() -> int:
    x, y, w, h = find_image('assets/monkey_money_earned.png')
    bounds = [x, y + h + 3, w, 50]
    bounds = [i.item() if not isinstance(i, int) else i for i in bounds] # assume numpy.int64, because it can do that for some fucking reason 
    text = int(ocr(bounds=bounds, threshold=(220, 255), invert=True).replace(' ', '').replace('\n', ''))
    return text

class Bot:
    def __init__(self, folder: str, restart: bool = False, queue = None) -> None:
        self.restart = restart
        self.stats = stats
        self.queue = queue
        with open(f'{folder}/setup.json', 'r') as fp:
            self.data: dict = json.load(fp)
        with open(f'{folder}/instructions.json', 'r') as fp:
            self.file: dict = json.load(fp)
    def setup(self) -> None:
        # TODO:
        # self.Setup.select_hero()
        select_map(self.data['MAP'], self.data['DIFFICULTY'], self.data['MODE'])
        while not find_current_screen() == 'in_game':
            pass
        block()
        if find_image('assets/screens/map_select_ok.png'):
            _click(960, 760)
            block(0.25)
    def _block_until_next_round_or_victory(self, current_round: int) -> None | int:
        while True:
            round = find_current_round()
            if round is not None and round != current_round:
                break
            img = find_many_images(images)
            match img:
                case 0: 
                    self.stats['games_won'] += 1
                    return 0
                case 1 | 2: _click(960, 540)
    def _parse_round(self) -> None | int:
        current_round = find_current_round()
        instructions = self.file.get(str(current_round))
        if instructions is not None:
            for instruction in instructions:
                parse_move(instruction)
                block()
        r = self._block_until_next_round_or_victory(current_round)
        if r == 0:
            return 0
    def gameloop(self) -> int | None:
        while True:
            try:
                r = self._parse_round()
                if r == 0:
                    return 0
            except:
                logger.error(traceback.format_exc())
                return 1
    def start(self):
        global towers
        self.setup()
        while True:
            start_time = time()
            r = self.gameloop()
            end_time = time()
            x, y, _, _ = find_image('assets/next.png')
            _click(x, y)
            block()
            self.stats['total_time'] += end_time - start_time
            self.stats['games_completed'] += 1
            self.stats['monkey_money_earned'] += find_monkey_money_earned()
            if self.queue is not None: self.queue.put(self.stats)
            if r == 0 and self.restart:
                restart_from_victory_screen()
                towers = Towers()
            else: break