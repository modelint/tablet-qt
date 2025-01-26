""" demo3_shapes.py - Test shape display """

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
        dtype = "Starr class diagram"
        # dtype = "xUML class diagram"
        # dtype = "xUML state machine diagram"
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo3_shapes.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="diagram", show_window=False, background_color='blue steel')


    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        vphrase = ["draws", "boundary with"]



        # TextElement.pin_block(layer=dlayer, asset='class face name', pin=Position(300,300), text=vphrase,
        #                       corner=TextBlockCorner.UR, align=HorizAlign.RIGHT)

        r = RectangleSE.add(layer=dlayer, asset="class name compartment", lower_left=Position(100, 100),
                            size=Rect_Size(height=27, width=253))
        # s = Symbol(layer=dlayer, name='final pseudo state', pin=Position(300, 300), angle=0)
        # s = Symbol(app='flatland', layer=dlayer, group='Starr class', name='M mult',
        #            pin=Position(400, 300), angle=0)

        DiagnosticMarker.add_raw_rectangle(layer=dlayer, upper_left=Position(10, 580),
                                           size=Rect_Size(width=800,height=580))
        DiagnosticMarker.add_cross_hair(layer=dlayer, location=Position(10, 580))
        # DiagnosticMarker.add_cross_hair(dlayer, Position(300, 275))
        cls.tablet.render()


if __name__ == "__main__":
    SketchSymbols.sketch()