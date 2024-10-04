""" line_segment.py -- Line Segment """

# System
import logging
from typing import TYPE_CHECKING

# Qt
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtCore import QLineF

# Tablet
import tabletqt.element as element
from tabletqt.geometry_types import Position
from tabletqt.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletqt.layer import Layer

_logger = logging.getLogger(__name__)
class LineSegment:
    """
    Manage the rendering of Line Segments

    Attributes and relationships defined on the class model

    Subclass of Shape Element on class model (R12)

    - ID {I} -- Element ID, unique within a Layer, implemented as object reference
    - Layer {I, R12} -- Element drawn on this Layer via R12/R15/Element/R19/Layer
    - From -- Draw from here in tablet coordinates
    - To -- To here in tablet coordinates
    """
    @classmethod
    def add(cls, layer: 'Layer', asset: str, from_here: Position, to_there: Position):
        """
        Convert line segment coordinates to device coordinates and combine with the Line Style defined
        for the Asset in the selected Preentation Style

        :param layer: Draw on this layer
        :param asset: Used to determine draw style
        :param from_here: In tablet coordinates
        :param to_there: In tablet coordinates
        """
        layer.Line_segments.append(
            element.Line_Segment(from_here=layer.Tablet.to_dc(from_here), to_there=layer.Tablet.to_dc(to_there),
                                 style=layer.Presentation.Shape_presentation[asset])
        )

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Draw the line segments

        :param layer: Draw on this layer
        """
        for ls in layer.Line_segments:
            _logger.info(f"> Line {ls.from_here}, {ls.to_there}")

            # Create a line item for the scene
            ls_item = QGraphicsLineItem(QLineF(*ls.from_here, *ls.to_there))
            CrayonBox.choose_crayons(item=ls_item, border_style=ls.style)
            layer.Scene.addItem(ls_item)
