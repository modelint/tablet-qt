""" symbol.py - Draw a predefined symbol """

# System
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsLineItem, QGraphicsItemGroup, QGraphicsEllipseItem
from PyQt6.QtCore import QPointF, QLineF, QRectF
from PyQt6.QtGui import QPolygonF
from typing import TYPE_CHECKING, Callable, Dict

# Tablet
from tabletqt.styledb import StyleDB
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletqt.tablet import Layer


class Symbol:
    """
    A composite group of shapes that can be rotated and placed anywhere on the Tablet on a specified Layer.
    """

    def __init__(self, app: str, layer: 'Layer', group: str, name: str, pin: Position, angle: int = 0):
        """
        Creates a Symbol that builds itself up from data specified in symbols.yaml and
            builds a PyQt group which is added to the layer's list of Symbols

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
        """
        self.app = app
        self.layer = layer
        self.group = group
        self.name = name
        self.pin = pin
        self.angle = angle
        self.width = 0
        self.height = 0
        self.shape_elements = StyleDB.symbol[app][group][name]
        self.symbol_item = QGraphicsItemGroup()

        self.shape_methods: Dict[str, Callable[[dict], None]] = {
            'triangle': self.add_triangle,
            'path': self.add_path,
            'circle': self.add_circle,
        }

        # Convert pin to device coordinates
        self.device_pin = layer.Tablet.to_dc(pin)

        # Add each component shape to the symbol_item
        for shape in self.shape_elements:
            for sname, method in self.shape_methods.items():
                if shape.get(sname):
                    method(shape)

        # Apply the rotation transform rotating on the pin position
        self.symbol_item.setTransformOriginPoint(self.device_pin.x, self.device_pin.y)
        self.symbol_item.setRotation(angle)

        # Add it to the supplied layer to be rendered in the correct stack order later
        self.layer.Symbols.append(self.symbol_item)

    def add_circle(self, shape):
        """

        :param shape:
        """
        center_canvas = Position(self.pin[0], shape['circle']['center'][1]+self.pin[1])
        # Flip lower left corner to device coordinates
        center_dc = self.layer.Tablet.to_dc(center_canvas)
        radius = shape['circle']['radius']
        diameter = radius * 2

        # Determine the bounding box size of the composite_shape
        self.width = max(self.width, diameter)
        self.height = max(self.height, diameter)

        # Create circle item
        circle_item = QGraphicsEllipseItem(QRectF(center_dc.x, center_dc.y, diameter, diameter))

        # Set pen and brush (border/fill) styles
        CrayonBox.choose_crayons(
            item=circle_item,
            border_style=shape['border'],
            fill=shape['fill'])

        # Add it to the supplied layer to be rendered in the correct stack order later
        self.symbol_item.addToGroup(circle_item)

    def add_path(self, shape):
        """

        :param shape:
        :return:
        """
        # Convert each vertex to a Position namedtuple
        canvas_vertices = [Position(v[0] + self.pin[0], v[1] + self.pin[1]) for v in shape['path']]

        # Determine the bounding box size of the symbol
        max_x = max(v[0] for v in shape['path'])
        max_y = max(v[1] for v in shape['path'])
        self.width = max(self.width, max_x)
        self.height = max(self.height, max_y)

        # Flip each vertex tablet Position to device coordinates
        device_vertices = [self.layer.Tablet.to_dc(v) for v in canvas_vertices]

        for v in range(len(device_vertices) - 1):
            start_point = device_vertices[v]
            end_point = device_vertices[v + 1]

            # Create a line item connecting the points
            line = QGraphicsLineItem(QLineF(*start_point, *end_point))
            # Set line style
            CrayonBox.choose_crayons(
                item=line,
                border_style=shape['border'])
            self.symbol_item.addToGroup(line)

    def add_triangle(self, shape):
        """

        :return:
        """
        # Convert each vertex to a Position namedtuple
        canvas_vertices = [Position(v[0] + self.pin[0], v[1] + self.pin[1]) for v in shape['triangle']]

        # Determine the bounding box size of the composite_shape
        max_x = max(v[0] for v in shape['triangle'])
        max_y = max(v[1] for v in shape['triangle'])
        self.width = max(self.width, max_x)
        self.height = max(self.height, max_y)

        # Flip each vertex tablet Position to device coordinates
        device_vertices = [self.layer.Tablet.to_dc(v) for v in canvas_vertices]
        pverts = [QPointF(*v) for v in device_vertices]
        polygon = QPolygonF(pverts)
        poly_item = QGraphicsPolygonItem(polygon)

        # Set pen and brush (border/fill) styles
        CrayonBox.choose_crayons(
            item=poly_item,
            border_style=shape['border'],
            fill=shape['fill'])

        # Add it to the supplied layer to be rendered in the correct stack order later
        self.symbol_item.addToGroup(poly_item)

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Add all symbols to the scene

        :param layer: Draw on this layer
        """
        for s in layer.Symbols:
            # _logger.info(f"> Polygon at: [{p.vertices}]")

            layer.Scene.addItem(s)

