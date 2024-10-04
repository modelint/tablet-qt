""" crayon_box.py - Sets the Qt pen and brush properties using the StyleDB """

# System
import logging
from typing import Optional

# Qt
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsLineItem

# Tablet
from tabletqt.styledb import StyleDB, Float_RGB

_logger = logging.getLogger(__name__)
class CrayonBox:
    """
    Get your crayons here. Specifically, your Qt pen and brush settings.
    """
    @classmethod
    def choose_crayons(cls, item: QAbstractGraphicsShapeItem | QGraphicsLineItem, border_style: str,
                       fill: Optional['str'] = None):
        """
        Create and assign a pen and brush for a given QT graphics item with settings found
        in the StyleDB

        :param item: Qt graphic item to be displayed
        :param border_style: Name of the user border style key in the StyleDB
        :param fill: Name of user fill key in the StyleDB, if any
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
                _logger.info(f"Brush color: [{fill}]")
            else:
                brush = QBrush(Qt.GlobalColor.transparent)
            item.setBrush(brush)

        # Set the item pen and brush of the graphic item
        item.setPen(pen)
        _logger.info(f"Pen color: [{cname}], width: [{w}], pattern: [{pname}]")

    @classmethod
    def choose_fill_only(cls, item: QAbstractGraphicsShapeItem, fill: Float_RGB):
        """
        Create and assign a transparent pen (no border) and brush for a given QT graphics item
        with settings found in the StyleDB.

        :param item: Qt graphic item to be displayed (must be a closed shape)
        :param fill: RGB color
        :return:
        """
        _logger.info(f"Brush color: {fill}")

        pen = QPen(Qt.GlobalColor.transparent)
        brush = QBrush(QColor(*fill))
        item.setPen(pen)
        item.setBrush(brush)