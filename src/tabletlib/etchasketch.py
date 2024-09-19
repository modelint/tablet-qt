""" etchasketch.py - Testbed for exercising the tablet with drawing patterns """

from pathlib import Path
from tabletlib.tablet import Tablet
from tabletlib.geometry_types import Rect_Size, Position


class EtchaSketch:

    tablet = None
    layer = None

    @classmethod
    def make_a_tablet(cls):
        size = Rect_Size(11*72, 17*72)  # 11x17 in points
        output_path = Path(__file__).parent.parent.parent / "working" / "sketch.pdf"
        cls.tablet = Tablet(size=size, output_file=output_path, drawing_type="xUML state machine diagram",
                            presentation="default", layer="diagram")

    @classmethod
    def draw_stuff(cls):
        cls.make_a_tablet()

        cls.tablet.layers['diagram'].add_rectangle(asset='state name only compartment', lower_left=Position(100, 200),
                                size=Rect_Size(100, 200))
        cls.tablet.render()



