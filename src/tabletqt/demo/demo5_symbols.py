""" demo5_symbols.py - Test symbol display """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign
from tabletqt.graphics.rectangle_se import RectangleSE
from tabletqt.graphics.diagnostic_marker import DiagnosticMarker

points_in_mm = 2.83465
points_in_cm = 28.3465
points_in_inch = 72


class SketchSymbols:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        cls.size = Rect_Size(round(210*points_in_mm), round(297*points_in_mm))  # Ansi C portrait
        dtype = "Starr class diagram"
        # dtype = "xUML class diagram"
        # dtype = "xUML state machine diagram"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo5_symbols.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')


    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']
        # State compartment test
        # llc = 1153.1, 1101.5
        # asset = state name compartment
        # size = 27h, 253w

        # s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 300), angle=0)
        s = Symbol(layer=dlayer, name='M mult', pin=Position(400, 300), angle=0)

        DiagnosticMarker.add_raw_rectangle(layer=dlayer, upper_left=Position(10, 580),
                                           size=Rect_Size(width=800,height=580))
        DiagnosticMarker.add_cross_hair(layer=dlayer, location=Position(10, 580))
        # DiagnosticMarker.add_cross_hair(dlayer, Position(300, 275))
        cls.tablet.render()


if __name__ == "__main__":
    SketchSymbols.sketch()