""" test_xuml_stickers.py - Draw all of the xuml class diagram stickers for different presentations """

import pytest
import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_xuml_stickers():
    dtype = "xUML class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='blue steel')
    dlayer = test_tablet.layers['diagram']

    TextElement.add_sticker(layer=dlayer, asset='class face name', name='1 mult',
                            pin=Position(150, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='M mult',
                            pin=Position(175, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='1c mult',
                            pin=Position(200, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='Mc mult',
                            pin=Position(250, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='association name', name='M mult',
                            pin=Position(300, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='superclass face name', name='superclass',
                            pin=Position(350, 400), corner=TextBlockCorner.LL)

    test_tablet.render()
    assert True

def test_bp_xuml_stickers():
    dtype = "xUML class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    TextElement.add_sticker(layer=dlayer, asset='class face name', name='1 mult',
                            pin=Position(150, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='M mult',
                            pin=Position(175, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='1c mult',
                            pin=Position(200, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='class face name', name='Mc mult',
                            pin=Position(250, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='association name', name='M mult',
                            pin=Position(300, 400), corner=TextBlockCorner.LL)
    TextElement.add_sticker(layer=dlayer, asset='superclass face name', name='superclass',
                            pin=Position(350, 400), corner=TextBlockCorner.LL)

    test_tablet.render()
    assert True

