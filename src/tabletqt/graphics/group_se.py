""" group_se.py -- Group Shape Element """

# System
import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tabletqt.layer import Layer

_logger = logging.getLogger(__name__)
class GroupSE:
    """
    """

    @classmethod
    def render(cls, layer: 'Layer'):
        """
        Draw the closed non-rectangular shapes

        :param layer: Draw on this layer
        """
        for g in layer.Groups:
            # _logger.info(f"> Polygon at: [{p.vertices}]")

            layer.Scene.addItem(g)