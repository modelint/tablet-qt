""" demo7_images - Test display of images """

from pathlib import Path
from tabletqt.tablet import Tablet
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.image import ImageDE

points_in_mm = 2.83465

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
        output_path = Path(__file__).parent.parent.parent.parent / "working" / "demo7_images.pdf"
        cls.tablet = Tablet(size=cls.size, output_file=output_path, drawing_type=dtype,
                            presentation="default", layer="diagram", show_window=False, background_color='blue steel')


    @classmethod
    def sketch(cls):

        cls.make_a_tablet()
        dlayer = cls.tablet.layers['diagram']

        ImageDE.add(layer=dlayer, name=f"mint-small", lower_left=Position(100,50), size=Rect_Size(180,24))
        ImageDE.add(layer=dlayer, name=f"mint-large", lower_left=Position(100,150), size=Rect_Size(191,25))
        ImageDE.add(layer=dlayer, name=f"MIT-small", lower_left=Position(100,350), size=Rect_Size(180,24))
        cls.tablet.render()


if __name__ == "__main__":
    SketchSymbols.sketch()