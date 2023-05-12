import logging


class ShipRadarLogger(logging.Logger):
    # Custom logging level, will output a lot
    VERBOSE = 5
    logging.VERBOSE = VERBOSE
    logging.Logger.VERBOSE = VERBOSE

    def __init__(self, name: str):
        super().__init__(name)
        # TODO add file handler, add better formatter
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.addLevelName(self.VERBOSE, "VERBOSE")

    def verbose(self, msg: str, *args, **kwargs):
        if self.isEnabledFor(self.VERBOSE):
            self._log(5, msg, args, **kwargs)



