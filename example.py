from src.bot import Bot
from src.bloons import is_game_focused
import src.logger as logger

import mouse
import multiprocessing
from time import sleep

def main():
    bot = Bot('macros/Infernal_Deflation', restart=True)
    if not is_game_focused():
        logger.info("Waiting for game to be focused...")
        while not is_game_focused():
            pass
    bot.start()

if __name__ == '__main__':
    bot_thread = multiprocessing.Process(target=main, args=(), daemon=True)
    bot_thread.start()
    try:
        while mouse.get_position() != (0,0) and bot_thread.is_alive():
            sleep(0.1)
        if bot_thread.is_alive():
            logger.error("Failsafe triggered!")
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        logger.info("Exiting...")
        bot_thread.terminate()