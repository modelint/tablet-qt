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
    def add(cls, app: str, layer: 'Layer', group: str, name: str, location: Position, angle: int) -> Rect_Size:
        symbol_data = StyleDB.symbol[app][group][name]
        for s in symbol_data:
            if s.get('triangle'):
                # Translate to spedified tablet location and make each vertex a Position named tuple
                canvas_vertices = [Position(v[0]+location[0], v[1]+location[1]) for v in s['triangle']]

                # Determine the rotation origin of the translated
                max_x = max(v[0] for v in s['triangle'])
                max_y = max(v[1] for v in s['triangle'])
                rot_origin = Position((max_x / 2) + location.x, location.y)
                device_rot_origin = layer.Tablet.to_dc(rot_origin)

                # Flip each position to device coordinates
                device_vertices = [layer.Tablet.to_dc(v) for v in canvas_vertices]
                pverts = [QPointF(*v) for v in device_vertices]
                polygon = QPolygonF(pverts)
                poly_item = QGraphicsPolygonItem(polygon)

                poly_item.setTransformOriginPoint(device_rot_origin.x, device_rot_origin.y)
                poly_item.setRotation(angle)

                CrayonBox.choose_crayons(
                    item=poly_item,
                    border_style=s['border'],
                    fill=s['fill'])

                layer.Polygons.append(poly_item)
                return Rect_Size(height=max_y,width=max_x)