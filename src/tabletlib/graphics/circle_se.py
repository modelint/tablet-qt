""" circle_se.py -- Circle shape element """

import logging
import tabletlib.element as element
from tabletlib.geometry_types import Position

from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtCore import QRectF
from typing import TYPE_CHECKING
from tabletlib.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletlib.layer import Layer

logger = logging.getLogger(__name__)
class CircleSE:
    """
    Manage the rendering of circle Shape Elements
    """

    @classmethod
    def add(cls, layer: 'Layer', asset: str, center: Position, radius: float):
        """
        Adds a circle to the layer and converts the center to device coordinates
        """
        # Flip lower left corner to device coordinates
        center_dc = layer.Tablet.to_dc(Position(x=center.x, y=center.y))

        # Check to see if this circle is filled
        fill = layer.Presentation.Closed_shape_fill.get(asset)

        layer.Circles.append(element.Circle(
            center=center_dc, radius=radius, border_style=layer.Presentation.Shape_presentation[asset], fill=fill,
        ))

    @classmethod
    def render(cls, layer: 'Layer'):
        """Draw the circle shapes"""

        for c in layer.Circles:

            # Create the circle item
            diameter = c.radius*2
            c_item = QGraphicsEllipseItem(QRectF(c.center.x, c.center.y, diameter, diameter))

            # Set pen and brush
            CrayonBox.choose_crayons(item=c_item, border_style=c.border_style, fill=c.fill)

            # Add it to the scene
            layer.Scene.addItem(c_item)

