""" line_segment.py -- Line Segment """

import logging
import tabletlib.element as element
from tabletlib.geometry_types import Position

from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtCore import QLineF
from typing import TYPE_CHECKING
from tabletlib.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletlib.layer import Layer

logger = logging.getLogger(__name__)
class LineSegment:
    """
    Manage the rendering of Line Segments
    """
    @classmethod
    def add(cls, layer: 'Layer', asset: str, from_here: Position, to_there: Position):
        """
        Convert line segment coordinates to device coordinates and combine with the Line Style defined
        for the Asset in the selected Preentation Style
        :param layer:
        :param asset:
        :param from_here:
        :param to_there:
        """
        layer.Line_segments.append(
            element.Line_Segment(from_here=layer.Tablet.to_dc(from_here), to_there=layer.Tablet.to_dc(to_there),
                                 style=layer.Presentation.Shape_presentation[asset])
        )

    @classmethod
    def render(cls, layer: 'Layer'):
        """Draw the line segments"""

        for ls in layer.Line_segments:

            # Create a line item for the scene
            ls_item = QGraphicsLineItem(QLineF(*ls.from_here, *ls.to_there))
            CrayonBox.choose_crayons(item=ls_item, border_style=ls.style)
            layer.Scene.addItem(ls_item)
