global logger
from loguru import logger
from loguru._logger import Logger


# class LogFilter:
#     """Insert logging level to logger on the fly
#     """
#     def __init__(self, level):
#         self.level = level

#     def __call__(self, record):
#         levelno = logger.level(self.level).no
#         return record["level"].no >= levelno
logger.remove()
# my_filter = LogFilter('DEBUG')
# logger.add(
#     sink='./logs/game.log',
#     filter=my_filter,
#     level=0,
#     format='{extra[game_name]} -> {extra[classname]}:"{extra[name]}" | {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
#     )
logger.disable('bgameb')


# class GameLogger:
#     """Set gamelogger
#     """

#     def __init__(
#         self,
#         log_path: str = './logs/game.log',
#         log_level: str = 'DEBUG'
#         ) -> None:
#         self.log_path = log_path,
#         self.log_level = log_level,
#         self.logger = logger

#     def get(self):
#         """Get logger

#         Returns:
#             _type_: _description_
#         """
#         self.logger.add(
#             sink=self.log_path,
#             level=self.log_level,
#             format='{extra[game_name]} -> {extra[classname]}:"{extra[name]}" | {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
#         )
#         self.logger.enable('bgameb')
#         return self.logger

def log_enable(
    logger: Logger = logger,
    log_path: str = './logs/game.log',
    log_level: str = 'DEBUG'
    ) -> None:
    """Enable logging

    Args:
        logger (Logger, optional): used logger. Defaults to logger.
        log_path (str, optional): path to log file. Defaults to './logs/game.log'.
        log_level (str, optional): logging level. Defaults to 'DEBUG'.
    """
    logger.add(
        sink=log_path,
        level=log_level,
        format='{extra[game_name]} -> {extra[classname]}:"{extra[name]}" | {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
    )
    logger.enable('bgameb')
