""" demo8_grid_rect.py - Test grid diagnostic boundary rect """

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
        dtype = "Grid Diagnostic"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo8_grid_rect.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="grid", show_window=False, background_color='white')

    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        glayer = cls.tablet.layers['grid']

        r = RectangleSE.add(layer=glayer, asset="grid boundary", lower_left=Position(10, 10),
                            size=Rect_Size(height=400, width=400))
        cls.tablet.render()

if __name__ == "__main__":
    SketchSymbols.sketch()
