""" rectangle_se.py -- Rectangle Shape Element """

# System
import logging
from typing import TYPE_CHECKING, Optional

# Qt
from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPainterPath

# Tablet
import tabletqt.element as element
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.styledb import StyleDB
from tabletqt.graphics.crayon_box import CrayonBox

if TYPE_CHECKING:
    from tabletqt.layer import Layer

_logger = logging.getLogger(__name__)

class RectangleSE:
    """
    Manage the rendering of Rectangle Shape Elements

    Attributes and relationships defined on the class model

    Subclass of Closed Shape on class model (R22)

    - ID {I} -- Element ID, unique within a Layer, implemented as object reference
    - Layer {I, R22} -- Element drawn on this Layer via R22/R12/R15/Element/R19/Layer
    - Size -- Rectangle height and width
    - Lower left -- Position of corner in tablet coordinates
    """
    @classmethod
    def add(cls, layer: 'Layer', asset: str, lower_left: Position, size: Rect_Size,
            color_usage: Optional['str'] = None):
        """
        Adds a rectangle to the Layer with position converted to Tablet (device) coordinates. If one is specified
        for this Shape Presentation (Presentation x Asset: See R4,R5,R21 in the class diagram), a Closed Shape Fill
        will be applied. If a color_usage is supplied, the associated color overrides the Closed Shape Fill.

        :param layer: Draw on this Layer
        :param asset: Used to determine draw style
        :param lower_left:  Lower left corner position in tablet coordinates
        :param size: The Size of the rectangle in points
        :param color_usage: If a usage string is provided, it will be indexed into the Style DB usage table to find
                            an associated RGB color.
        """
        # Flip lower left corner to device coordinates
        ll_dc = layer.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # If a fill is predefined for this presentation/shape asset, get it
        fill = layer.Presentation.Closed_shape_fill.get(asset)

        # Now see if there is an overriding color usage, if so use the corresponding color instead
        if color_usage:
            try:
                fill = StyleDB.color_usage[color_usage]  # Overrides any closed shape fill
            except KeyError:
                _logger.warning(f'No color defined for usage [{color_usage}]')

        # Set the corner spec, if any
        cspec = layer.Presentation.Corner_spec.get(asset)
        # If no corner spec, assume 0 radius corners
        radius, top, bottom = (0, False, False) if not cspec else (cspec.radius, cspec.top, cspec.bottom)

        layer.Rectangles.append(element.Rectangle(
            upper_left=ul, size=size, border_style=layer.Presentation.Shape_presentation[asset], fill=fill,
            radius=radius, top=top, bottom=bottom
        ))

    @classmethod
    def roundrect(cls, x: float, y: float, width: float, height: float, top_r: int, bottom_r: int) -> QGraphicsPathItem:
        """
        Draw rectangle with rounded corners on top, bottom or both. Radius is expressed in points
        with zero resulting in a square corner on top, bottom or both

        :param x: Upper left x
        :param y: Upper left y
        :param width: Rect width
        :param height: Rect height
        :param top_r: Top corner radius
        :param bottom_r: Bottom corner radius
        """
        rect = QRectF(x, y, width, height)
        path = QPainterPath()

        if top_r and bottom_r:
            path.addRoundedRect(rect, bottom_r, bottom_r)

        if top_r and not bottom_r:
            path.moveTo(rect.topLeft() + QPointF(top_r, 0))
            path.arcTo(rect.left(), rect.top(), top_r * 2, top_r * 2, 90, 90)
            path.moveTo(rect.topLeft() + QPointF(top_r, 0))
            path.lineTo(rect.right() - top_r * 2, rect.top())
            path.arcTo(rect.right() - top_r * 2, rect.top(), top_r * 2, top_r * 2, 90, -90)
            path.moveTo(rect.right(), rect.top() + top_r)
            path.lineTo(rect.bottomRight())
            path.lineTo(rect.bottomLeft())
            path.lineTo(rect.left(), rect.top() + top_r)

        if bottom_r and not top_r:
            path.moveTo(rect.left(), rect.bottom() - bottom_r)
            path.lineTo(rect.topLeft())
            path.lineTo(rect.topRight())
            path.lineTo(rect.right(), rect.bottom() - bottom_r)
            path.arcTo(rect.right() - bottom_r * 2, rect.bottom() - bottom_r * 2, bottom_r * 2, bottom_r * 2, 0, -90)
            path.moveTo(rect.right() - bottom_r, rect.bottom())
            path.lineTo(rect.left() + bottom_r, rect.bottom())
            path.arcTo(rect.left(), rect.bottom() - bottom_r * 2, bottom_r * 2, bottom_r * 2, 270, -90)

        return QGraphicsPathItem(path)

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Draw all rectangle shapes added to a Layer

        :param layer: Draw on this Layer
        """
        for r in layer.Rectangles:
            # Diagnostic shaded rectangle bounding box under the rendered rectangle
            # to see if the corners are drawn correctly
            # frame = QGraphicsRectItem(QRectF(r.upper_left.x, r.upper_left.y, r.size.width, r.size.height))
            # fpen = QPen(Qt.GlobalColor.blue)
            # fbrush = QBrush(Qt.GlobalColor.lightGray)
            # frame.setBrush(fbrush)
            # frame.setPen(fpen)
            # layer.Scene.addItem(frame)

            # Set rectangle extents and draw
            top_radius = r.radius if r.top else 0
            bottom_radius = r.radius if r.bottom else 0
            path = cls.roundrect(r.upper_left.x, r.upper_left.y, r.size.width, r.size.height, top_radius, bottom_radius)
            _logger.info(f"> Roundrect at: {r.upper_left}, size: {r.size},"
                         f"top round: {top_radius}, bottom_round: {bottom_radius}")
            # Set pen and brush
            CrayonBox.choose_crayons(item=path, border_style=r.border_style, fill=r.fill)
            layer.Scene.addItem(path)

    @classmethod
    def render_fillrect(cls, layer: 'Layer', frect: element.FillRect):
        """
        Render a single specified filled retangle

        For now, this feature is not directly available to the user. It is used
        on demand as a component of other elements such as text to create an
        opaque underlay.

        :param layer: Draw on this layer
        :param frect: The fill color
        """
        # Create the rect item
        rect = QRectF(frect.upper_left.x, frect.upper_left.y, frect.size.width, frect.size.height)
        r_item = QGraphicsRectItem(rect)
        _logger.info(f"> Filled rect at: {frect.upper_left}, size: {frect.size}")

        # Set pen and brush
        CrayonBox.choose_fill_only(item=r_item, fill=frect.color)
        layer.Scene.addItem(r_item)
