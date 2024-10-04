""" etchasketch.py - Testbed for exercising the tabletqt with drawing patterns """

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


class EtchaSketch:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        # size = Rect_Size(11*72, 17*72) # Ansi D
        cls.size = Rect_Size(17 * 72, 22 * 72)  # Ansi C h=1224 x w=1584
        # size = Rect_Size(22*72, 34*72) # Ansi D
        output_path = Path(__file__).parent.parent.parent / "working" / "tabletqt.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type="xUML state machine diagram",
                            presentation="default", layer="diagram")

    @classmethod
    def draw_stuff(cls):
        cls.make_a_tablet()

        dlayer = cls.tablet.layers['diagram']

        slayer = cls.tablet.add_layer(name='sheet', presentation='default', drawing_type="OS Engineer large frame")

        RectangleSE.add(layer=dlayer, asset='state name only compartment',
                        lower_left=Position(50, 700), size=Rect_Size(height=20, width=70))

        PolygonSE.add(layer=dlayer, asset='solid arrow', vertices=[
            Position(300, 300),
            Position(320, 340),
            Position(340, 300)
        ])

        ImageE.add(layer=slayer, resource_path=Path("mint_logo_medium.png"),
                   lower_left=Position(1150, 50), size=Rect_Size(10, 10))

        # RectangleSE.add(layer=dlayer, asset='state name only compartment', lower_left=Position(200, 600),
        #                                            size=Rect_Size(30, 150))

        pad = 0
        # Horizontal top
        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(pad, cls.size.height),
                        to_there=Position(cls.size.width, cls.size.height))

        # Horizontal bottom
        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(pad, pad),
                        to_there=Position(cls.size.width, pad))
        # vertical left
        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(pad, cls.size.height),
                        to_there=Position(pad, pad))

        # vertical right
        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(cls.size.width, cls.size.height),
                        to_there=Position(cls.size.width, pad))

        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(510, 400), to_there=Position(510, 600))

        LineSegment.add(layer=dlayer, asset='transition connector',
                        from_here=Position(230, 580), to_there=Position(230, 200))

        CircleSE.add(layer=dlayer, asset='solid small dot', center=Position(400, 400), radius=20)

        # General location reference
        DiagnosticMarker.add_cross_hair(dlayer, Position(200, 500))
        DiagnosticMarker.add_cross_hair(dlayer, Position(200, 600))
        DiagnosticMarker.add_cross_hair(dlayer, Position(200, 700))

        # Print this text
        # sample_text = "Thirty seven goodies"
        # cls.tabletqt.layers['diagram'].add_text_line(
        #     asset='transition name', lower_left=Position(255, 623), text=sample_text)
        sample_text = "Thirty seven goodies"
        TextElement.add_line(layer=dlayer,
                             asset='state name', lower_left=Position(215, 300), text=sample_text)

        DiagnosticMarker.add_cross_hair(dlayer, Position(498, 712), 'purple')
        # Get the tbox size
        # tbox = cls.tabletqt.layers['diagram'].text_line_size(asset='transition name', text_line=sample_text)
        tbox = TextElement.line_size(layer=dlayer, asset='state name', text_line=sample_text)

        # Draw cross hairs where the displayed text should line up
        DiagnosticMarker.add_cross_hair(dlayer, Position(255, 623), 'green')  # Lower left of text
        DiagnosticMarker.add_cross_hair(dlayer, Position(255, 623 + tbox.height), 'green')  # Upper left of text

        # Put bounding box at the upper left crosshair
        DiagnosticMarker.add_raw_rectangle(layer=dlayer, upper_left=Position(255, 623 + tbox.height),
                                           size=Rect_Size(tbox.height, tbox.width))

        pad_x = 5  # To adjust the position of the bounding rectangle relative to the text upper left corner
        pad_y = -4
        # cls.tabletqt.layers['diagram'].add_raw_rectangle(upper_left=Position(255, 635+pad_y),
        #                                                size=Rect_Size(tbox.height, tbox.width))
        # DiagnosticMarker.add_cross_hair(layer=dlayer, Position(255, 635)) # Upper left of text
        #
        # DiagnosticMarker.add_cross_hair(layer=dlayer, Position(5, 5))
        # DiagnosticMarker.add_cross_hair(layer=dlayer, Position(255, 623), 'green') # Lower left of text
        # DiagnosticMarker.add_cross_hair(layer=dlayer, Position(255, 623+tbox.height), 'red')  # Upper left of text

        # Lower left of text block
        DiagnosticMarker.add_cross_hair(dlayer, Position(500, 500), 'green')
        TextElement.add_block(layer=dlayer, asset='transition name', lower_left=Position(500, 500),
                              text=['From here', 'to quick goats'])
        tbox = TextElement.text_block_size(layer=dlayer, asset='transition name',
                                           text_block=['From here', 'to quick goats'])
        # cls.tabletqt.layers['diagram'].add_raw_rectangle(upper_left=Position(500, 500+tbox.height),
        #                                                size=Rect_Size(tbox.height, tbox.width))

        cls.tablet.render()
