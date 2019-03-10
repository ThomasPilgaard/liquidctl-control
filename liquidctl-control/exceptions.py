class Error(Exception):
    pass

class FanNotConnectedException(Error):
    """Raised when a given fan is not connected to the fan controller"""

    def __init__(self, message):
        self.message = message

