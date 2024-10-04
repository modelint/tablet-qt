"""
exceptions.py – Tabletx exceptions
"""

class TabletException(Exception):
    pass

class BadConfigData(TabletException):
    pass

class NonSystemInitialLayer(TabletException):
    pass

class TabletBoundsExceeded(TabletException):
    pass
