"""
This module contains all custom exceptions used in the ShipRadar project.
"""


class ShipRadarBaseException(Exception):
    """
    Base exception for ShipRadar
    """
    def __init__(self, reason: str):
        super().__init__(reason)


class ShipRadarImportError(ShipRadarBaseException, OSError):
    """
    Raised when there is a general error importing data
    or when the data is not in the correct format
    """
    def __init__(self, additional: str = "No additional information"):
        super().__init__(f"Error importing data: {additional}")


class ShipRadarFilterError(ShipRadarImportError):
    """
    Raised when there is an error filtering data
    """
    def __init__(self, reason: str):
        super().__init__(reason)
