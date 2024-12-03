""" symbol.py - Draw a predefined symbol """

from tabletqt.styledb import StyleDB
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.graphics.polygon_se import PolygonSE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tabletqt.tablet import Layer


class Symbol:
    pass

    @classmethod
    def draw(cls, app: str, layer: 'Layer', group: str, name: str, position: Position, angle: int) -> Rect_Size:
        symbol_data = StyleDB.symbol[app][group][name]
        for s in symbol_data:
            if s.get('triangle'):
                PolygonSE.add(layer=layer, asset=)
                pass
            pass