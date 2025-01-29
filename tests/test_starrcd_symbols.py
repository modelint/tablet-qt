""" test_starrcd_symbols.py - Draw all of the Starr class diagram symbols for different presentation """

import pytest
import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_starrcd_symbols():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='autumn')
    dlayer = test_tablet.layers['diagram']

    s = Symbol(layer=dlayer, name='ordinal', pin=Position(50, 400), angle=0)
    s = Symbol(layer=dlayer, name='1 mult', pin=Position(75, 400), angle=0)
    s = Symbol(layer=dlayer, name='M mult', pin=Position(100, 400), angle=0)
    s = Symbol(layer=dlayer, name='1c mult', pin=Position(125, 400), angle=0)
    s = Symbol(layer=dlayer, name='Mc mult', pin=Position(150, 400), angle=0)
    s = Symbol(layer=dlayer, name='superclass', pin=Position(175, 400), angle=0)

    s = Symbol(layer=dlayer, name='ordinal', pin=Position(50, 300), angle=90)
    s = Symbol(layer=dlayer, name='1 mult', pin=Position(75, 300), angle=90)
    s = Symbol(layer=dlayer, name='M mult', pin=Position(100, 300), angle=90)
    s = Symbol(layer=dlayer, name='1c mult', pin=Position(125, 300), angle=90)
    s = Symbol(layer=dlayer, name='Mc mult', pin=Position(150, 300), angle=90)
    s = Symbol(layer=dlayer, name='superclass', pin=Position(175, 300), angle=90)

    test_tablet.render()
    assert True

def test_bp_starrcd_symbols():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    s = Symbol(layer=dlayer, name='ordinal', pin=Position(50, 400), angle=0)
    s = Symbol(layer=dlayer, name='1 mult', pin=Position(75, 400), angle=0)
    s = Symbol(layer=dlayer, name='M mult', pin=Position(100, 400), angle=0)
    s = Symbol(layer=dlayer, name='1c mult', pin=Position(125, 400), angle=0)
    s = Symbol(layer=dlayer, name='Mc mult', pin=Position(150, 400), angle=0)
    s = Symbol(layer=dlayer, name='superclass', pin=Position(175, 400), angle=0)

    s = Symbol(layer=dlayer, name='ordinal', pin=Position(50, 300), angle=90)
    s = Symbol(layer=dlayer, name='1 mult', pin=Position(75, 300), angle=90)
    s = Symbol(layer=dlayer, name='M mult', pin=Position(100, 300), angle=90)
    s = Symbol(layer=dlayer, name='1c mult', pin=Position(125, 300), angle=90)
    s = Symbol(layer=dlayer, name='Mc mult', pin=Position(150, 300), angle=90)
    s = Symbol(layer=dlayer, name='superclass', pin=Position(175, 300), angle=90)

    test_tablet.render()
    assert True

