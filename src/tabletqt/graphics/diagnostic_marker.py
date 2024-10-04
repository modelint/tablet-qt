""" diagnostic_marker.py -- Diagnostic marking """

from tabletqt.geometry_types import Position, Rect_Size

from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QLineF
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPen, QColor

if TYPE_CHECKING:
    from tabletqt.layer import Layer


class DiagnosticMarker:
    """
    Manage the rendering of diagnostic markers such as crosshairs, rectangles
    and other shapes drawn with explicitly specified styles.

    (The StyleDB is not consulted for any of these)
    """
    ch_radius = 3  # Cross hair radius

    @classmethod
    def add_cross_hair(cls, layer: 'Layer', location: Position, color: str = 'black'):
        """
        Place a diagnostic cross hair at the requested point in the Scene.
        This method is not intended for client application use.

        :param color:
        :param location: Where to place the crosshair in application coordinates
        """
        pen = QPen(QColor(color), 1)
        # Flip to device coordinates
        ll_dc = layer.Tablet.to_dc(Position(x=location.x, y=location.y))
        hline = QGraphicsLineItem(QLineF(ll_dc.x-cls.ch_radius, ll_dc.y, ll_dc.x+cls.ch_radius, ll_dc.y))
        hline.setPen(pen)
        vline = QGraphicsLineItem(QLineF(ll_dc.x, ll_dc.y-cls.ch_radius, ll_dc.x, ll_dc.y+cls.ch_radius))
        vline.setPen(pen)
        layer.RawLines.append(hline)
        layer.RawLines.append(vline)

    @classmethod
    def add_raw_rectangle(cls, layer: 'Layer', upper_left: Position, size: Rect_Size):
        """
        Adds an unfilled rectangle for diagnostic purposes. 'raw' means that the dimensions
        are supplied directly without consulting the StyleDB

        :param upper_left:
        :param size:
        :return:
        """
        # Use upper left corner instead
        # ul = Position(x=upper_left.x, y=upper_left.y - size.height)

        # Convert upper left corner to device coordinates
        uldc = layer.Tablet.to_dc(Position(x=upper_left.x, y=upper_left.y))

        rect = QRectF(uldc.x, uldc.y, size.width, size.height)
        rect_item = QGraphicsRectItem(rect)
        layer.RawRectangles.append(rect_item)

    @classmethod
    def render(cls, layer: 'Layer'):

        # Render all raw lines
        for l in layer.RawLines:
            layer.Scene.addItem(l)

        # Render all raw rectangles
        pen = QPen(QColor(0, 0, 0))
        for r in layer.RawRectangles:
            r.setPen(pen)
            layer.Scene.addItem(r)
