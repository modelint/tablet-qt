""" test_rectangles.py - Draw some rectangle shapes for different presentations on the diagram layer """

import pytest
import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.rectangle_se import RectangleSE

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_class_compartment():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='blue steel')
    dlayer = test_tablet.layers['diagram']

    r = RectangleSE.add(layer=dlayer, asset="class name compartment", lower_left=Position(100, 100),
                        size=Rect_Size(height=27, width=253))
    test_tablet.render()
    assert True

def test_bp_class_compartment():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    r = RectangleSE.add(layer=dlayer, asset="imported class attribute compartment", lower_left=Position(100, 100),
                        size=Rect_Size(height=27, width=253))
    test_tablet.render()
    assert True

def test_state_compartment():
    dtype = "xUML state machine diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='autumn')
    dlayer = test_tablet.layers['diagram']

    r = RectangleSE.add(layer=dlayer, asset="state name only compartment", lower_left=Position(100, 100),
                        size=Rect_Size(height=27, width=253))
    test_tablet.render()
    assert True
def test_bp_state_compartment():
    dtype = "xUML state machine diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')
    dlayer = test_tablet.layers['diagram']

    r = RectangleSE.add(layer=dlayer, asset="state name only compartment", lower_left=Position(100, 100),
                        size=Rect_Size(height=27, width=253))
    test_tablet.render()
    assert True
