""" sticker.py -- Sticker """

# System
import logging
from pathlib import Path
from typing import TYPE_CHECKING

# Modelint
from mi_config.config import Config

# Tablet
from tabletqt.graphics.text_element import TextElement
from tabletqt.geometry_types import Position
from tabletqt.styledb import StyleDB

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
        """

        """
        sticker_data = Config(app_name='mi_tablet', lib_config_dir=config_dir, fspec={'stickers':None})
        cls.names = sticker_data.loaded_data['stickers']

    @classmethod
    def add(cls, layer: 'Layer', asset: str, name: str, pin: Position):
        """

        :param layer:
        :param asset:
        :param group:
        :param name:
        :param pin:
        :return:
        """
        app = layer.Tablet.client_app_name
        sticker_text = cls.names[app][layer.Drawing_type][asset][name]
        TextElement.add_line(layer=layer, asset=asset, lower_left=pin, text=sticker_text)
