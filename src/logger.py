import logging


class ShipRadarLogger(logging.Logger):
    VERBOSE = 5
    logging.VERBOSE = VERBOSE
    logging.Logger.VERBOSE = VERBOSE

    def __init__(self, name: str):
        super().__init__(name)
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.addLevelName(self.VERBOSE, "VERBOSE")

    def verbose(self, msg: str, *args, **kwargs):
        if self.isEnabledFor(self.VERBOSE):
            self._log(5, msg, args, **kwargs)



