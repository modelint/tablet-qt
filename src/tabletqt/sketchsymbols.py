""" sketchsymbols.py - Testbed for exercising the tabletqt with predefined symbols """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.rectangle_se import RectangleSE
from tabletqt.symbol import Symbol

points_in_mm = 2.83465
points_in_cm = 28.3465
points_in_inch = 72

class SketchSymbols:
    tablet = None
    layer = None
    size = None

    @classmethod
    def make_a_tablet(cls):
        cls.size = Rect_Size(17*72, 22*72)  # Ansi C portrait
        dtype = "Starr Class Diagram"
        output_path = Path(__file__).parent.parent.parent / "working" / "tabletqt.pdf"
        cls.tablet = Tablet(app='flatland', size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="diagram", background_color='white')

    @classmethod
    def sketch(cls):
        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        Symbol.add(app='flatland', layer=dlayer, group='Starr class', name='1 mult', location=Position(700, 700), angle=270)

        RectangleSE.add(layer=dlayer, asset='class attribute compartment',
                        lower_left=Position(50, 300), size=Rect_Size(height=20, width=70))
        cls.tablet.render()

