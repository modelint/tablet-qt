"""
exceptions.py – Tabletx exceptions
"""

class TabletException(Exception):
    pass

class BadConfigData(TabletException):
    pass

class MissingConfigData(TabletException):
    pass

class NonSystemInitialLayer(TabletException):
    pass

class TabletBoundsExceeded(TabletException):
    def __init__(self, message, height, width):
        self.message = message
        self.height = height
        self.width = width
        super().__init__(f"{message} (Height exceeded: {height} Width exceeded: {width})")

