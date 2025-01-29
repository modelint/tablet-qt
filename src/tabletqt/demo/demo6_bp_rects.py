""" demo6_bp_rects.py - Test rectangles using blueprint presentation """

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
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo6_bp_rects.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')

    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        r = RectangleSE.add(layer=dlayer, asset="imported class attribute compartment", lower_left=Position(100, 100),
                            size=Rect_Size(height=27, width=253))
        cls.tablet.render()

if __name__ == "__main__":
    SketchSymbols.sketch()
