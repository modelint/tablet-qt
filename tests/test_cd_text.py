""" test_cd_text.py - Draw class diagram text blocks """

import pytest
import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_cd_text():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='blue steel')
    dlayer = test_tablet.layers['diagram']

    vphrase = ["draws", "boundary with"]

    TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(200,300), text=vphrase,
                          corner=TextBlockCorner.UR, align=HorizAlign.RIGHT)

    TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(300,300), text=vphrase,
                          corner=TextBlockCorner.UR, align=HorizAlign.LEFT)
    test_tablet.render()
    assert True

def test_bp_cd_text():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    vphrase = ["draws", "boundary with"]

    TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(200,300), text=vphrase,
                          corner=TextBlockCorner.UR, align=HorizAlign.RIGHT)

    TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(300,300), text=vphrase,
                          corner=TextBlockCorner.UR, align=HorizAlign.LEFT)
    test_tablet.render()
    assert True
