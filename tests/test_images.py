""" test_xuml_stickers.py - Draw all of the xuml class diagram stickers for different presentations """

import inspect
from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.image import ImageDE

points_in_mm = 2.83465
A4 = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))

def test_images():
    dtype = "Starr class diagram"
    function_name = inspect.currentframe().f_code.co_name
    output_path = Path(f"output/{function_name}.pdf")

    test_tablet = Tablet(size=A4, output_file=output_path, drawing_type=dtype,
                         presentation="default", layer="diagram", show_window=False, background_color='blue steel')
    dlayer = test_tablet.layers['diagram']

    ImageDE.add(layer=dlayer, name=f"mint-small", lower_left=Position(100, 50), size=Rect_Size(180, 24))
    ImageDE.add(layer=dlayer, name=f"mint-large", lower_left=Position(100, 150), size=Rect_Size(191, 25))
    ImageDE.add(layer=dlayer, name=f"MIT-small", lower_left=Position(100, 350), size=Rect_Size(180, 24))

    test_tablet.render()
    assert True
