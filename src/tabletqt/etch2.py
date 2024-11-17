""" etch2.py - Testbed for exercising the tabletqt with drawing patterns """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.circle_se import CircleSE
from tabletqt.graphics.polygon_se import PolygonSE
from tabletqt.graphics.line_segment import LineSegment
from tabletqt.graphics.rectangle_se import RectangleSE
from tabletqt.graphics.image import ImageE
from tabletqt.graphics.text_element import TextElement
from tabletqt.graphics.diagnostic_marker import DiagnosticMarker


class Etch2:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        # size = Rect_Size(11*72, 17*72) # Ansi D
        cls.size = Rect_Size(17 * 72, 22 * 72)  # Ansi C h=1224 x w=1584
        # size = Rect_Size(22*72, 34*72) # Ansi D
        output_path = Path(__file__).parent.parent.parent / "working" / "tabletqt.pdf"
        # cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type="OS Engineer large frame",
        #                     presentation="default", layer="sheet")
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type="OS Engineer large frame",
                            presentation="default", layer="diagram")

    @classmethod
    def draw_stuff(cls):
        cls.make_a_tablet()

        slayer = cls.tablet.layers['diagram']

        ImageE.add(layer=slayer, resource_path=Path("mint_logo_medium.png"),
                   lower_left=Position(1150, 50), size=Rect_Size(10, 10))
        # RectangleSE.add(layer=slayer, asset='Block border',
        #                 lower_left=Position(1150, 150), size=Rect_Size(100, 300))
        RectangleSE.add(layer=slayer, asset='box',
                        lower_left=Position(1150, 150), size=Rect_Size(100, 300))
        pad = 0
        # Horizontal to
        LineSegment.add(layer=slayer, asset='Block border',
                        from_here=Position(pad, cls.size.height),
                        to_there=Position(cls.size.width, cls.size.height))
        # Horizontal bottom
        LineSegment.add(layer=slayer, asset='Block border',
                        from_here=Position(pad, pad),
                        to_there=Position(cls.size.width, pad))
        # vertical left
        LineSegment.add(layer=slayer, asset='Block border',
                        from_here=Position(pad, cls.size.height),
                        to_there=Position(pad, pad))

        # vertical right
        LineSegment.add(layer=slayer, asset='Block border',
                        from_here=Position(cls.size.width, cls.size.height),
                        to_there=Position(cls.size.width, pad))

        cls.tablet.render()
