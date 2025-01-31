""" demo6_bp_text.py - Test rectangles using blueprint presentation """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign
from tabletqt.graphics.line_segment import LineSegment

points_in_mm = 2.83465


class SketchSymbols:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        cls.size = Rect_Size(round(210 * points_in_mm), round(297 * points_in_mm))  # Ansi C portrait
        dtype = "xUML class diagram"
        # dtype = "Starr class diagram"
        # dtype = "xUML state machine diagram"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo9_underlay.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="diagram", show_window=False, background_color='blue steel')

    @classmethod
    def sketch(cls):
        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        # LineSegment.add(layer=dlayer, asset="binary association connector",
        #                 from_here=Position(100,305), to_there=Position(400,305))

        LineSegment.add(layer=dlayer, asset="binary association connector",
                        from_here=Position(100,305), to_there=Position(400,305))

        TextElement.add_sticker(layer=dlayer, asset='superclass face name', name='superclass',
                                pin=Position(300, 300), corner=TextBlockCorner.LL)
        # TextElement.add_block(layer=dlayer, asset='superclass face name', lower_left=Position(300, 300), text=['underlay'])

        cls.tablet.render()


if __name__ == "__main__":
    SketchSymbols.sketch()
