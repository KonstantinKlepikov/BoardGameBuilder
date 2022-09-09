"""Utils, like logger
"""
from loguru import logger
from loguru._logger import Logger
from random_word import RandomWords


global log_me
log_me: Logger = logger
log_me.disable('bgameb')

rw = RandomWords()


def log_enable(
    log_path: str = './logs/game.log',
    log_level: str = 'DEBUG'
        ) -> None:
    """Enable logging

    Args:
        log_path (str, optional): path to log file.
                                  Defaults to './logs/game.log'.
        log_level (str, optional): logging level. Defaults to 'DEBUG'.
    """
    log_me.remove()
    log_me.add(
        sink=log_path,
        level=log_level,
        format='{extra[classname]}: "{extra[name]}" -> func {function} | ' +
        '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
    )
    log_me.enable('bgameb')

def get_random_name(max_lenght: int = 10) -> str:
    """Get english word of given len

    Returns:
        str: random word
    """
    def roll():

        result = rw.get_random_word(
            minLength=6,
            maxLength=max_lenght,
            includePartOfSpeech='noun',
            )
        if not result:
            result = roll()

        return result

    return roll()
