""" etchasketch.py - Testbed for exercising the tablet with drawing patterns """

from pathlib import Path
from tabletlib.tablet import Tablet
from tabletlib.geometry_types import Rect_Size, Position


class EtchaSketch:

    tablet = None
    layer = None

    @classmethod
    def make_a_tablet(cls):
        # size = Rect_Size(11*72, 17*72) # Ansi D
        size = Rect_Size(17*72, 22*72) # Ansi C
        # size = Rect_Size(22*72, 34*72) # Ansi D
        output_path = Path(__file__).parent.parent.parent / "working" / "sketch.pdf"
        cls.tablet = Tablet(size=size, output_file=output_path, drawing_type="xUML state machine diagram",
                            presentation="default", layer="diagram")

    @classmethod
    def draw_stuff(cls):
        cls.make_a_tablet()

        cls.tablet.add_layer(name='sheet', presentation='default', drawing_type="OS Engineer large frame",
                             fill="dead leaf")

        cls.tablet.layers['diagram'].add_rectangle(asset='state name only compartment', lower_left=Position(200, 600),
                                size=Rect_Size(30, 150))

        cls.tablet.layers['diagram'].add_text_line(asset='state name', lower_left=Position(255, 623), text="Idle")
        cls.tablet.render()



