"""
Contains ShipRadarLogger class, responsible for logging.
"""

import logging


class ShipRadarLogger(logging.Logger):
    """
    Custom logger class, inherits from logging.Logger.
    """
    # Custom logging level, will output a lot
    VERBOSE: int = 5

    def __init__(self, name: str = __name__):
        super().__init__(name)
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        __fmt: str = "%(asctime)s, %(name)s: %(levelname)s - %(message)s"
        __fmt_date: str = "%d-%b-%y %H:%M:%S"
        self._formatter = logging.Formatter(__fmt, __fmt_date)

        self.stdout_handler = logging.StreamHandler()
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.setFormatter(self._formatter)
        self.addHandler(self.stdout_handler)

        self.file_handler = logging.FileHandler("shipradar.log")
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self._formatter)
        self.addHandler(self.file_handler)

    def verbose(self, msg: str, *args, **kwargs):
        """
        Log a message with severity 'VERBOSE' on the root logger.
        :param msg: message to log
        :param args: arguments to pass to logger
        :param kwargs: keyword arguments to pass to logger
        :return:
        """
        if self.isEnabledFor(self.VERBOSE):
            self._log(5, msg, args, **kwargs)
