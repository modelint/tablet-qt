""" etchasketch.py - Testbed for exercising the tablet with drawing patterns """

from pathlib import Path
from tabletlib.tablet import Tablet
from tabletlib.geometry_types import Rect_Size, Position


class EtchaSketch:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        # size = Rect_Size(11*72, 17*72) # Ansi D
        cls.size = Rect_Size(17 * 72, 22 * 72)  # Ansi C h=1224 x w=1584
        # size = Rect_Size(22*72, 34*72) # Ansi D
        output_path = Path(__file__).parent.parent.parent / "working" / "sketch.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type="xUML state machine diagram",
                            presentation="default", layer="diagram")

    @classmethod
    def draw_stuff(cls):
        cls.make_a_tablet()

        cls.tablet.add_layer(name='sheet', presentation='default', drawing_type="OS Engineer large frame",
                             fill="white")

        cls.tablet.layers['diagram'].add_polygon(asset='solid arrow', vertices=[
            Position(300, 300),
            Position(320, 340),
            Position(340, 300)
        ])


        cls.tablet.layers['diagram'].add_image(resource_path=Path("mint_logo_medium.png"),
                                               lower_left=Position(1150,50), size=Rect_Size(10,10))

        # cls.tablet.layers['diagram'].add_rectangle(asset='state name only compartment', lower_left=Position(200, 600),
        #                                            size=Rect_Size(30, 150))

        pad = 0
        # Horizontal top
        cls.tablet.layers['diagram'].add_line_segment(asset='transition connector',
                                                      from_here=Position(pad,cls.size.height),
                                                      to_there=Position(cls.size.width,cls.size.height))
        # Horizontal bottom
        cls.tablet.layers['diagram'].add_line_segment(asset='transition connector',
                                                      from_here=Position(pad,pad),
                                                      to_there=Position(cls.size.width,pad))
        # vertical left
        cls.tablet.layers['diagram'].add_line_segment(asset='transition connector',
                                                      from_here=Position(pad,cls.size.height),
                                                      to_there=Position(pad,pad))

        # vertical right
        cls.tablet.layers['diagram'].add_line_segment(asset='transition connector',
                                                      from_here=Position(cls.size.width,cls.size.height),
                                                      to_there=Position(cls.size.width,pad))

        cls.tablet.layers['diagram'].add_line_segment(asset='transition connector',
                                                      from_here=Position(230,580), to_there=Position(230,200))

        cls.tablet.layers['diagram'].add_circle(asset='solid small dot', center=Position(400, 400), radius=20)

        # General location reference
        cls.tablet.layers['diagram'].add_cross_hair(Position(200, 500), 'black')
        cls.tablet.layers['diagram'].add_cross_hair(Position(200, 600), 'black')
        cls.tablet.layers['diagram'].add_cross_hair(Position(200, 700), 'black')

        # Print this text
        # sample_text = "Thirty seven goodies"
        # cls.tablet.layers['diagram'].add_text_line(
        #     asset='transition name', lower_left=Position(255, 623), text=sample_text)
        sample_text = "Thirty seven goodies"
        cls.tablet.layers['diagram'].add_text_line(
            asset='state name', lower_left=Position(255, 623), text=sample_text)

        # Get the tbox size
        # tbox = cls.tablet.layers['diagram'].text_line_size(asset='transition name', text_line=sample_text)
        tbox = cls.tablet.layers['diagram'].text_line_size(asset='state name', text_line=sample_text)

        # Draw cross hairs where the displayed text should line up
        cls.tablet.layers['diagram'].add_cross_hair(Position(255, 623), 'green') # Lower left of text
        cls.tablet.layers['diagram'].add_cross_hair(Position(255, 623+tbox.height), 'green')  # Upper left of text

        # Put bounding box at the upper left crosshair
        cls.tablet.layers['diagram'].add_raw_rectangle(upper_left=Position(255, 623+tbox.height),
                                                       size=Rect_Size(tbox.height, tbox.width))


        pad_x = 5  # To adjust the position of the bounding rectangle relative to the text upper left corner
        pad_y = -4
        # cls.tablet.layers['diagram'].add_raw_rectangle(upper_left=Position(255, 635+pad_y),
        #                                                size=Rect_Size(tbox.height, tbox.width))
        # cls.tablet.layers['diagram'].add_cross_hair(Position(255, 635)) # Upper left of text
        #
        # cls.tablet.layers['diagram'].add_cross_hair(Position(5, 5))
        # cls.tablet.layers['diagram'].add_cross_hair(Position(255, 623), 'green') # Lower left of text
        # cls.tablet.layers['diagram'].add_cross_hair(Position(255, 623+tbox.height), 'red')  # Upper left of text

        cls.tablet.render()
