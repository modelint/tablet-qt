""" demo6_bp_text.py - Test rectangles using blueprint presentation """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.text_element import TextElement, TextBlockCorner, HorizAlign

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
        # dtype = "Starr class diagram"
        dtype = "xUML class diagram"
        # dtype = "xUML state machine diagram"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo6_bp_text.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="blueprint", layer="diagram", show_window=False, background_color='blueprint')

    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        # vphrase = ["draws", "boundary with"]
        #
        # TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(300,300), text=vphrase,
        #                       corner=TextBlockCorner.UR, align=HorizAlign.RIGHT)

        TextElement.add_sticker(layer=dlayer, asset='class face name', name='1c mult',
                                pin=Position(300, 300), corner=TextBlockCorner.LL)

        cls.tablet.render()

if __name__ == "__main__":
    SketchSymbols.sketch()
