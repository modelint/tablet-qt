""" polygon_se.py -- Polygon Shape Element """

# System
import logging
from typing import TYPE_CHECKING, List

# Qt
from PyQt6.QtWidgets import QGraphicsPolygonItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

# Tablet
import tabletqt.element as element
from tabletqt.geometry_types import Position
from tabletqt.graphics.crayon_box import CrayonBox
from tabletqt.graphics.line_segment import LineSegment

if TYPE_CHECKING:
    from tabletqt.layer import Layer

_logger = logging.getLogger(__name__)
class PolygonSE:
    """
    Manage the rendering of Polygon Shape Elements which are Closed Shapes

    Additionally, a contiguous sequence of Line Segements are managed here as an
    open polygon shape. There is no concept of an open polygon in the class models so
    the add_open method could just as easily be part of the Line Segment Element class.
    In fact, there is no enforced constraint that the segments be contiguous.

    (The idea was to support drawing a pattern like an open arrow head).

    For legacy reasons, let's just leave it here for now.

    Attributes and relationships defined on the class model

    Subclass of Closed Shape on class model (R22)
    Related via {R17} to an ordered set of Vertex instances
    These are implemented as a supplied list of tablet positions

    - ID {I} -- Element ID, unique within a Layer, implemented as object reference
    - Layer {I, R22} -- Element drawn on this Layer via R22/R12/R15/Element/R19/Layer
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
        Rather than manage a seperate render open polygon list in the Layer, we
        can just add these to the line segment list.

        :param layer: Draw on this layer
        :param asset: Used to look up the line style
        :param vertices: A sequences of 2 or more vertices
        """
        for v1, v2 in zip(vertices, vertices[1:]):
            assert len(vertices) > 1, "Open polygon has less than two vertices"
            LineSegment.add(layer=layer, asset=asset, from_here=v1, to_there=v2)

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Draw the closed non-rectangular shapes

        :param layer: Draw on this layer
        """
        for p in layer.Polygons:
            _logger.info(f"> Polygon at: [{p.vertices}]")

            pverts = [QPointF(*x) for x in p.vertices]
            polygon = QPolygonF(pverts)
            poly_item = QGraphicsPolygonItem(polygon)

            # Set pen and brush
            CrayonBox.choose_crayons(item=poly_item, border_style=p.border_style, fill=p.fill)

            layer.Scene.addItem(poly_item)
