""" circle_se.py -- Circle shape element """

# System
import logging
from typing import TYPE_CHECKING

# Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtCore import QRectF

# Tablet
import tabletqt.element as element
from tabletqt.geometry_types import Position
from tabletqt.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletqt.layer import Layer

_logger = logging.getLogger(__name__)
class CircleSE:
    """
    Manage the rendering of Circle Shape Elements

    Attributes and relationships defined on the class model

    Subclass of Closed Shape on class model (R22)

    - ID {I} -- Element ID, unique within a Layer, implemented as object reference
    - Layer {I, R22} -- Element drawn on this Layer via R22/R12/R15/Element/R19/Layer
    - Radius -- Circle radius
    - Center -- Position of center in tablet coordinates
    """

    @classmethod
    def add(cls, layer: 'Layer', asset: str, center: Position, radius: float):
        """
        Adds a circle to the layer and converts the center to device coordinates

        :param layer: Draw on this layer
        :param asset: Used to look up the border style
        :param center: The center position in tablet coordinates
        :param radius: The radius length in points
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
        """
        Draw the circle shapes

        :param layer: Draw on this layer
        """

        for c in layer.Circles:

            # Create the circle item
            diameter = c.radius*2
            c_item = QGraphicsEllipseItem(QRectF(c.center.x, c.center.y, diameter, diameter))
            _logger.info(f"> Circle at: ({c.center.x}, {c.center.y}), diameter: {diameter}")

            # Set pen and brush
            CrayonBox.choose_crayons(item=c_item, border_style=c.border_style, fill=c.fill)

            # Add it to the scene
            layer.Scene.addItem(c_item)

