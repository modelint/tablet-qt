""" demo8_grid_rect.py - Test grid diagnostic boundary rect """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign
from tabletqt.graphics.rectangle_se import RectangleSE
from tabletqt.graphics.line_segment import LineSegment
from tabletqt.graphics.diagnostic_marker import DiagnosticMarker
from tabletqt.exceptions import TabletBoundsExceeded

points_in_mm = 2.83465

class SketchSymbols:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        cls.size = Rect_Size(height=round(841*points_in_mm), width=round(1189*points_in_mm))  # Ansi C portrait
        dtype = "Grid Diagnostic"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo8_grid_rect.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="grid", show_window=False, background_color='white')

    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        glayer = cls.tablet.layers['grid']

        try:
            LineSegment.add(layer=glayer, asset="row boundary", from_here=Position(210, 2398.64),
                            to_there=Position(2772, 2398.6499))
        except TabletBoundsExceeded as e:
            pass

        # r = RectangleSE.add(layer=glayer, asset="grid boundary", lower_left=Position(2398.64, 210),
        #                     size=Rect_Size(height=2398.64, width=210))
        cls.tablet.render()

if __name__ == "__main__":
    SketchSymbols.sketch()
