""" image.py -- Image element """

# System
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tabletqt.layer import Layer

# Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

# Modelint
from mi_config.config import Config

# Tablet
import tabletqt.element as element
from tabletqt.geometry_types import Position, Rect_Size
from tabletqt.exceptions import TabletBoundsExceeded
from tabletqt.styledb import StyleDB
from tabletqt.tablet_config import TabletConfig

_logger = logging.getLogger(__name__)

class ImageDE:
    """
    Image Display Element
    (subclass of Rectangular Display Element in Render Subsystem not shown on model yet)

    Manage the loading and rendering of Image Elements

    Attributes and relationships defined on the class model

    (Not currently in the class model, but will be added)

    Subclass of Element on class model (R15) - most likely

    - ID {I} -- Element ID, unique within a Layer, implemented as object reference
    - Layer {I, R22} -- Element drawn on this Layer via R22/R12/R15/Element/R19/Layer
    - Location -- Path to the image file
    - Lower left -- Position of the lower left image corner in tablet coordinates
    - Size -- The actual size of the image in the file
    """
    image_paths = None

    @classmethod
    def build_paths(cls):
        """ Assign image file dictionary """
        raw_config_data = Config(app_name=TabletConfig.app_name, lib_config_dir=TabletConfig.config_path, fspec={'images': None})
        image_dict = raw_config_data.loaded_data['images']
        root_dir = raw_config_data.user_config_dir
        cls.image_paths = {k: Path(root_dir / 'images' / v) for k,v in image_dict.items()}


    @classmethod
    def add(cls, layer: 'Layer', name: str, lower_left: Position, size: Rect_Size):
        """
        Adds the image to the layer, converting to device coordinates and using the upper
        left corner of the image instead to suit Qt placement

        :param layer: Draw on this Layer
        :param name: Name of the image resource supplied by the client
        :param size: The actual size of the image in points
        :param lower_left:  Lower left corner of the image in tablet coordinates
        """

        # Flip lower left corner to device coordinates
        try:
            ll_dc = layer.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))
        except TabletBoundsExceeded:
            _logger.warning(f"Lower left corner of image [{image_path}] is outside Tablet draw region")
            return

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # Add it to the list
        try:
            layer.Images.append(element.Image(resource_path=cls.image_paths[name], upper_left=ul, size=size))
        except KeyError:
            _logger.warning(f"No path defined for image [{name}]")
        else:
            _logger.info(f'View>> Layer {layer.Name} registered resource at: {cls.image_paths[name]}')

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Render the Image Elements

        :param layer: Draw on this Layer
        """
        for i in layer.Images:
            if not i.resource_path.exists():
                _logger.error(f'Image file [{i.resource_path}] not found')
                continue

            pixmap = QPixmap(str(i.resource_path))
            if pixmap.isNull():
                _logger.error(f'Image file [{i.resource_path}] could not be loaded as pixmap')
                continue

            pix_item = QGraphicsPixmapItem(pixmap)
            pix_item.setPos(i.upper_left.x, i.upper_left.y)
            layer.Scene.addItem(pix_item)
            _logger.info(f"> Image at: ({i.upper_left.x}, {i.upper_left.y})")
