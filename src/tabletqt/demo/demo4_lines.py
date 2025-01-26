""" demo4_lines.py - Test line display """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.symbol import Symbol
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign
from tabletqt.graphics.line_segment import LineSegment
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
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo4_lines.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="diagram", show_window=False, background_color='blue steel')


    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        line = LineSegment.add(layer=dlayer, asset="binary association connector",
                               from_here=Position(100,100), to_there=Position(100,300))

        DiagnosticMarker.add_raw_rectangle(layer=dlayer, upper_left=Position(10, 580),
                                           size=Rect_Size(width=800,height=580))
        DiagnosticMarker.add_cross_hair(layer=dlayer, location=Position(10, 580))
        # DiagnosticMarker.add_cross_hair(dlayer, Position(300, 275))
        cls.tablet.render()


if __name__ == "__main__":
    SketchSymbols.sketch()