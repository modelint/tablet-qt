""" image.py -- Image element """

import logging
import tabletlib.element as element
from tabletlib.geometry_types import Position, Rect_Size
from tabletlib.exceptions import TabletBoundsExceeded

from pathlib import Path
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tabletlib.layer import Layer

logger = logging.getLogger(__name__)

class ImageE:
    """
    Manage the loading and rendering of Image Elements
    """
    @classmethod
    def add(cls, layer: 'Layer', resource_path: Path, lower_left: Position, size: Rect_Size):
        """
        Adds the image

        :param size:
        :param resource_path: Path to an image file
        :param lower_left:  Lower left corner of the image in Cartesian coordinates
        """
        # Flip lower left corner to device coordinates
        try:
            ll_dc = layer.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))
        except TabletBoundsExceeded:
            logger.warning(f"Lower left corner of image [{resource_path.name}] is outside Tablet draw region")
            return

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # Add it to the list
        layer.Images.append(element.Image(resource_path=resource_path, upper_left=ul, size=size))
        logger.info(f'View>> Layer {layer.Name} registered resource at: {resource_path}')

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Render the Image Elements

        :param layer: Draw on this Layer
        """

        for i in layer.Images:
            if not i.resource_path.exists():
                logger.error(f'Image file [{i.resource_path}] not found')
                continue

            pixmap = QPixmap(str(i.resource_path))
            if pixmap.isNull():
                logger.error(f'Image file [{i.resource_path}] could not be loaded as pixmap')
                continue

            pix_item = QGraphicsPixmapItem(pixmap)
            pix_item.setPos(i.upper_left.x, i.upper_left.y)
            layer.Scene.addItem(pix_item)
