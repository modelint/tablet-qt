""" symbol.py - Draw a predefined symbol """

# System
from PyQt6.QtWidgets import QGraphicsPolygonItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF
from typing import TYPE_CHECKING

# Tablet
from tabletqt.styledb import StyleDB
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.polygon_se import PolygonSE
from tabletqt.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletqt.tablet import Layer


class Symbol:
    pass

    @classmethod
    def add(cls, app: str, layer: 'Layer', group: str, name: str, pin: Position, angle: int) -> Rect_Size:
        """
        Places, translates, and rotates a symbol defined in the symbols.yaml file.

        :param app: Name of the client application, ex: 'flatland', (needed to index into symbol data)
        :param layer: Layer where symbol will be drawn ex: 'diagram'
        :param group: Symbol belongs to this group (diagram type/notation if flatland), ex: Starr class
        :param name: Symbol name (1 mult, target state, etc)
        :param pin: Where the symbol will be 'pinned' in table coordinates. Imagine a pin pushed through the
        bottom of the symbol bounding box into the tablet. Then the symbol can be rotated around this pin. So
        if you are placing a double headed arrow with the arrow pointing upward in the symbol definition,
        for example, you pin the center base and then rotate the arrows leaving the base center in the same
        location regardless of rotation. In other words, the client need not compute the bounding box to determine
        the pin location.
        :param angle: Degrees clockwise with 0, 90, 180, and 270 at 12, 3, 6, and 9 o'clock respectively
        :return: The size of the total symbol bounding box
        """
        # Look up the symbol
        width = 0
        height = 0
        shape_elements = StyleDB.symbol[app][group][name]
        for shape in shape_elements :
            if shape.get('triangle'):

                # Convert each vertex to a Position namedtuple
                canvas_vertices = [Position(v[0] + pin[0], v[1] + pin[1]) for v in shape['triangle']]

                # Determine the bounding box size of the symbol
                max_x = max(v[0] for v in shape['triangle'])
                max_y = max(v[1] for v in shape['triangle'])
                width = max(width, max_x)
                height = max(height, max_y)

                # Convert pin to device coordinates
                device_pin = layer.Tablet.to_dc(pin)

                # Flip each vertex tablet Position to device coordinates
                device_vertices = [layer.Tablet.to_dc(v) for v in canvas_vertices]
                pverts = [QPointF(*v) for v in device_vertices]
                polygon = QPolygonF(pverts)
                poly_item = QGraphicsPolygonItem(polygon)

                # Apply the rotation transform rotating on the pin position
                poly_item.setTransformOriginPoint(device_pin.x, device_pin.y)
                poly_item.setRotation(angle)

                # Set pen and brush (border/fill) styles
                CrayonBox.choose_crayons(
                    item=poly_item,
                    border_style=shape['border'],
                    fill=shape['fill'])

                # Add it to the supplied layer to be rendered in the correct stack order later
                layer.Polygons.append(poly_item)

        return Rect_Size(height=height,width=width)