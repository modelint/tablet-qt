""" polygon_se.py -- Polygon Shape Element """

import logging
import tabletlib.element as element
from tabletlib.geometry_types import Position

from PyQt6.QtWidgets import QGraphicsPolygonItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF
from typing import TYPE_CHECKING, List
from tabletlib.graphics.crayon_box import CrayonBox
from tabletlib.graphics.line_segment import LineSegment

if TYPE_CHECKING:
    from tabletlib.layer import Layer

_logger = logging.getLogger(__name__)
class PolygonSE:
    """
    Manage the rendering of Polygon Shape Elements
    """

    @classmethod
    def add(cls, layer: 'Layer', asset: str, vertices: List[Position]):
        """
        Add a closed polygon to the layer

        :param layer: Draw on this layer
        :param asset: Used to determine draw style
        :param vertices: Polygon vertices in Tablet coordinates
        """
        # Flip each position to device coordinates
        device_vertices = [layer.Tablet.to_dc(v) for v in vertices]

        layer.Polygons.append(element.Polygon(
            vertices= device_vertices,
            border_style=layer.Presentation.Shape_presentation[asset],
            fill=layer.Presentation.Closed_shape_fill[asset]
        ))

    @classmethod
    def add_open(cls, layer: 'Layer', asset: str, vertices: List[Position]):
        """
        Add all of the line segments necessary to draw the polygon to our list of line segments

        :param layer: Draw on this layer
        :param asset: Used to look up the line style
        :param vertices: A sequences of 2 or more vertices
        """
        for v1, v2 in zip(vertices, vertices[1:]):
            assert len(vertices) > 1, "Open polygon has less than two vertices"
            LineSegment.add(layer=layer, asset=asset, from_here=v1, to_there=v2)

    @classmethod
    def render(cls, layer: 'Layer'):
        """Draw the closed non-rectangular shapes"""
        for p in layer.Polygons:
            _logger.info(f"> Polygon at: [{p.vertices}]")

            pverts = [QPointF(*x) for x in p.vertices]
            polygon = QPolygonF(pverts)
            poly_item = QGraphicsPolygonItem(polygon)

            # Set pen and brush
            CrayonBox.choose_crayons(item=poly_item, border_style=p.border_style, fill=p.fill)

            layer.Scene.addItem(poly_item)
