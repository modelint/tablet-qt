"""
layer.py - Layer of content drawn on a Tablet
"""
import logging
import tabletlib.element as element
from tabletlib.presentation import Presentation
from graphics.circle_se import CircleSE
from graphics.polygonSE import PolygonSE
from graphics.line_segment import LineSegment
from graphics.rectangle_se import RectangleSE
from graphics.text_element import TextElement
from graphics.image import ImageE
from graphics.diagnostic_marker import DiagnosticMarker
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsLineItem

if TYPE_CHECKING:
    from tabletlib.tablet import Tablet

class Layer:
    """
    A common feature of many drawing and image editing applications is the ability to stack layers of
    content along a z axis toward the user’s viewpoint. Similarly, the Tablet renders each layer working
    from the lowest value on the z axis toward the highest. Thus, content on the higher layers may overlap
    content underneath.

        Attributes

        - Line_segments -- A list of geometric lines each with start and end coordinates.
        - Rectangles -- A list of rectangles each with a lower left corner, height and width
        - Polygons -- A list of closed polygons
        - Text -- A list of text lines (new lines are not supported)
    """

    def __init__(self, name: str, tablet: 'Tablet', presentation: str, drawing_type: str):
        """
        Constructor

        :param name: The Layer name
        :param tablet: The Tablet object
        :param presentation: Presentation to be applied to this Layer
        :param drawing_type: The Presentation's View Type
        :param fill: A color to fill the drawing area
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"creating layer: [{name}] ")
        self.Name = name
        self.Tablet = tablet
        self.Scene = tablet.View.scene  # This is what we actually draw on
        self.Drawing_type = drawing_type

        # Stuff we will draw on the Layer
        self.Line_segments: List[element.Line_Segment] = []
        self.Circles: List[element.Circle] = []
        self.Polygons: List[element.Polygon] = []
        self.Rectangles: List[element.Rectangle] = []
        self.RawRectangles: List[QGraphicsRectItem] = []
        self.RawLines: List[QGraphicsLineItem] = []
        self.TextUnderlayRects: List[element.FillRect] = []
        self.Text: List[element.Text_line] = []
        self.Images: List[element.Image] = []

        # Load this Layer's presentation assets if they haven't been already
        # Unique ID (see Tablet Subsystem class diagram) of a Presentation is both
        # its name and its View Type name.  So we combine them to form the index
        pres_index = ':'.join([self.Drawing_type, presentation])
        self.Presentation = self.Tablet.Presentations.get(pres_index)
        if not self.Presentation:
            # It hasn't been loaded from the Flatland DB yet
            self.Presentation = Presentation(name=presentation, drawing_type=self.Drawing_type)
            self.Tablet.Presentations[pres_index] = self.Presentation


    def render(self):
        """Renders all Elements on this Layer"""

        self.logger.info(f'Rendering layer: {self.Name}')

        # Rendering order determines what can potentially overlap on this Layer, so order matters
        LineSegment.render(self)
        CircleSE.render(self)
        RectangleSE.render(self)
        PolygonSE.render(self)
        TextElement.render_underlays(self)  # Renders any color fills that lie underneath text blocks or lines
        TextElement.render(self)  # Render text after vector content so that it is never underneath
        ImageE.render(self)  # Text should not be drawn over images, so we can render these last

        # Diagnostic elements with explicit styling that bypass StyleDB lookup
        # Not intended for use by any client applications
        DiagnosticMarker.render(self)


