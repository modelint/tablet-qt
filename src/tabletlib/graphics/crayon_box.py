""" crayon_box.py - Sets the Qt pen and brush properties using the StyleDB """

import sys
import logging

from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsLineItem
from tabletlib.styledb import StyleDB
from typing import Optional

logger = logging.getLogger(__name__)
class CrayonBox:
    """
    Get your crayons here. Specifically, your Qt pen and brush settings.
    """
    @classmethod
    def choose_crayons(cls, item: QAbstractGraphicsShapeItem | QGraphicsLineItem, border_style: str,
                       fill: Optional['str'] = None):
        """
        :param item: Sets the pen properties of this item
        :param border_style: Name of the border style used to index StyleDB
        :param fill: Name of fill, if any
        """
        # Create a pen and set its properties using the StyleDB
        # Color
        cname = StyleDB.line_style[border_style].color
        c_color = StyleDB.rgbF[cname]
        # Width
        w = StyleDB.line_style[border_style].width
        pen = QPen(QColor(*c_color), w)
        # Pattern
        pname = StyleDB.line_style[border_style].pattern  # name of line style's pattern
        if pname != 'no dash':
            pvalue = StyleDB.dash_pattern[pname]  # find pattern value in dash pattern dict
            pen.setDashPattern([*pvalue])

        if isinstance(item, QAbstractGraphicsShapeItem):
            # item is fillable, not a line item, for example
            if fill:
                # If a fill is specified, create a corresponding brush
                fill_rgb_color_value = StyleDB.rgbF[fill]
                brush = QBrush(QColor(*fill_rgb_color_value))
            else:
                brush = QBrush(Qt.GlobalColor.transparent)
            item.setBrush(brush)

        # Set the item pen and brush of the graphic item
        item.setPen(pen)

    @classmethod
    def choose_fill_only(cls, item: QAbstractGraphicsShapeItem, fill: 'str'):
        """
        Set fill with a transparent pen

        :param item:
        :param fill:
        :return:
        """
        # Lookup the RGB color value from the user color name
        try:
            fill_rgb_color_value = StyleDB.rgbF[fill]
        except KeyError:
            logger.error(f'Fill rect color [{fill}] not defined in system or user configuration')
            sys.exit(1)

        pen = QPen(Qt.GlobalColor.transparent)
        brush = QBrush(QColor(*fill_rgb_color_value))
        item.setPen(pen)
        item.setBrush(brush)