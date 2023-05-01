
class ShipRadarBaseException(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)


class ShipRadarImportError(ShipRadarBaseException, OSError):
    pass


class ShipRadarFilterError(ShipRadarImportError):
    def __init__(self, reason: str):
        super().__init__(reason)
