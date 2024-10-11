""" styles.py - Named tuples representing various style data """

from typing import NamedTuple

class ColorCanvas(NamedTuple):
    r: int
    g: int
    b: int
    canvas : bool

class FloatRGB(NamedTuple):
    r: int
    g: int
    b: int

class LineStyle(NamedTuple):
    pattern: str
    width: int
    color: str

class TextStyle(NamedTuple):
    typeface: str
    size: int
    slant: str
    weight: str
    color: str
    spacing: float

class DashPattern(NamedTuple):
    solid: float
    blank: float
