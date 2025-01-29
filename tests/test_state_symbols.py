""" test_state_symbols.py - Draw all of the state machine symbols for different presentation """

import pytest
import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_state_symbols():
    dtype = "xUML state machine diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='autumn')
    dlayer = test_tablet.layers['diagram']

    s = Symbol(layer=dlayer, name='target state', pin=Position(100, 200), angle=0)
    s = Symbol(layer=dlayer, name='initial pseudo state', pin=Position(200, 200), angle=0)
    s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 200), angle=0)

    s = Symbol(layer=dlayer, name='target state', pin=Position(100, 400), angle=90)
    s = Symbol(layer=dlayer, name='initial pseudo state', pin=Position(200, 400), angle=180)
    s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 400), angle=270)

    test_tablet.render()
    assert True

def test_bp_state_symbols():
    dtype = "xUML state machine diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    s = Symbol(layer=dlayer, name='target state', pin=Position(100, 200), angle=0)
    s = Symbol(layer=dlayer, name='initial pseudo state', pin=Position(200, 200), angle=0)
    s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 200), angle=0)

    s = Symbol(layer=dlayer, name='target state', pin=Position(100, 400), angle=90)
    s = Symbol(layer=dlayer, name='initial pseudo state', pin=Position(200, 400), angle=180)
    s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 400), angle=270)

    test_tablet.render()
    assert True

