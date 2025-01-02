""" symbol.py - Draw a predefined symbol """

# System
import logging
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsLineItem, QGraphicsItemGroup, QGraphicsEllipseItem
from PyQt6.QtCore import QPointF, QLineF, QRectF
from PyQt6.QtGui import QPolygonF
from typing import TYPE_CHECKING, Callable, Dict

# Tablet
from tabletqt.styledb import StyleDB
from tabletqt.geometry_types import Position
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
        self.logger = logging.getLogger(__name__)
        self.app = app
        self.layer = layer
        self.group = group
        self.name = name
        self.pin = pin
        self.angle = angle
        self.width = 0
        self.height = 0
        try:
            self.shape_elements = StyleDB.symbol[app][group][name]
        except KeyError:
            self.logger.exception(f"StyleDB has no entry for: [{app}][{group}][{name}]")
            return

        self.symbol_item = QGraphicsItemGroup()

        # These are the shape elements currently supported
        # TODO: Add rectangles and images
        self.shape_methods: Dict[str, Callable[[dict], None]] = {
            'triangle': self.add_triangle,
            'path': self.add_path,
            'circle': self.add_circle,
        }

        # Convert pin to device coordinates
        self.device_pin = layer.Tablet.to_dc(pin)

        # Create item for each component shape element, position it on the tablet, and add it to a Qt
        # symbol item group for any transforms to be applied to the entire symbol
        for shape in self.shape_elements:
            for sname, method in self.shape_methods.items():
                if shape.get(sname):
                    method(shape)  # Call method apporpriate to the shape

        # Create the rotation transform and apply it to the group
        self.symbol_item.setTransformOriginPoint(self.device_pin.x, self.device_pin.y)
        self.symbol_item.setRotation(angle)

        # Add it the transformed group to the Symbols list in the specified layer of the tablet
        # for later rendering
        self.layer.Symbols.append(self.symbol_item)


    def add_circle(self, shape: Dict):
        """
        Adds a circle shape element to the symbol item group

        :param shape: The shape definition obtained from the symbol yaml file for this circle
        """
        # Translate center in symbol bounding box relative to the pin
        # We just add the center position to the pin position to translate the circle
        center_tablet = Position(self.pin[0]+shape['circle']['center'][0], self.pin[1]+shape['circle']['center'][1])

        # Convert center tablet to device coordinates
        center_dc = self.layer.Tablet.to_dc(center_tablet)
        radius = shape['circle']['radius']
        diameter = radius * 2

        # Update dimensions of the bounding box if either dimension is larger
        self.width = max(self.width, diameter)
        self.height = max(self.height, diameter)

        # Create Qt circle item
        # We subtract the radius since Qt wants the top left corner for positioning
        circle_item = QGraphicsEllipseItem(QRectF(center_dc.x-radius, center_dc.y-radius, diameter, diameter))

        # Set pen and brush (border/fill) styles
        CrayonBox.choose_crayons(
            item=circle_item,
            border_style=shape['border'],
            fill=shape['fill'])

        # Add circle shape element to the symbol item group
        self.symbol_item.addToGroup(circle_item)

    def add_path(self, shape):
        """
        Adds a path element (series of connected line segments) to the symbol item group

        :param shape: The shape definition obtained from the symbol yaml file for this path
        """
        # Translate each vertex relative to the pin
        # We just add the pin to vertex coordinates
        canvas_vertices = [Position(v[0] + self.pin[0], v[1] + self.pin[1]) for v in shape['path']]

        # Update dimensions of the bounding box if any vertex is outside the current dimensions
        max_x = max(v[0] for v in shape['path'])
        max_y = max(v[1] for v in shape['path'])
        self.width = max(self.width, max_x)
        self.height = max(self.height, max_y)

        # Convert vertices to device coordinates
        vertices_dc = [self.layer.Tablet.to_dc(v) for v in canvas_vertices]

        # Create a line item connecting gap between each pair of vertices
        # from beginning of vertex list to the last vertex in the list
        # and add the line item to the symbol item group
        for v in range(len(vertices_dc) - 1):
            start_point = vertices_dc[v]
            end_point = vertices_dc[v + 1]

            # Create a line item connecting the points
            line = QGraphicsLineItem(QLineF(*start_point, *end_point))

            # Set line style
            CrayonBox.choose_crayons(
                item=line,
                border_style=shape['border'])

            # Add line to the symbol item group
            self.symbol_item.addToGroup(line)

    def add_triangle(self, shape):
        """
        Adds a triangle shape element to the symbol item group

        :param shape: The shape definition obtained from the symbol yaml file for this triangle
        """
        # TODO: generalize this to handle any polygon
        # Translate each vertex relative to the pin
        # We just add the pin to vertex coordinates
        canvas_vertices = [Position(v[0] + self.pin[0], v[1] + self.pin[1]) for v in shape['triangle']]

        # Update dimensions of the bounding box if any vertex is outside the current dimensions
        max_x = max(v[0] for v in shape['triangle'])
        max_y = max(v[1] for v in shape['triangle'])
        self.width = max(self.width, max_x)
        self.height = max(self.height, max_y)

        # Convert vertices to device coordinates
        vertices_dc = [self.layer.Tablet.to_dc(v) for v in canvas_vertices]

        # Create a polygon item
        pverts = [QPointF(*v) for v in vertices_dc]
        polygon = QPolygonF(pverts)
        poly_item = QGraphicsPolygonItem(polygon)

        # Set pen and brush (border/fill) styles
        CrayonBox.choose_crayons(
            item=poly_item,
            border_style=shape['border'],
            fill=shape['fill'])

        # Add triangle to the symbol item group
        self.symbol_item.addToGroup(poly_item)

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Add each symbol item group to the Scene for display

        :param layer: Draw on this layer
        """
        for s in layer.Symbols:
            # _logger.info(f"> Polygon at: [{p.vertices}]")

            # Display the item in the Qt scene
            layer.Scene.addItem(s)

