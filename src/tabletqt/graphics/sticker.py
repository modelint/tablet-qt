""" sticker.py -- Sticker """

# System
import logging
from pathlib import Path
from typing import TYPE_CHECKING

# Modelint
from mi_config.config import Config

# Tablet
# import tabletqt.element as element
# from tabletqt.geometry_types import Position, Rect_Size, HorizAlign
# from tabletqt.styledb import StyleDB
# from tabletqt.exceptions import TabletBoundsExceeded

if TYPE_CHECKING:
    from tabletqt.layer import Layer

logger = logging.getLogger(__name__)
config_dir = Path(__file__).parent / "configuration"

class Sticker:
    """
    Display a text sticker
    """
    names = None

    @classmethod
    def load_names(cls):
        sticker_data = Config(app_name='mi_tablet', lib_config_dir=config_dir, fspec={'stickers':None})
        cls.names = sticker_data.loaded_data['stickers']
        pass

    @classmethod
    def add_sticker(cls, layer: 'Layer', asset: str, group: str, name: str, lower_left: Position):
    #     pass
