""" text_element.py -- Text Element """

import logging
import tabletlib.element as element
from tabletlib.geometry_types import Position, Rect_Size, HorizAlign
from tabletlib.styledb import StyleDB
from tabletlib.exceptions import TabletBoundsExceeded

from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QFontMetrics, QColor
from typing import TYPE_CHECKING, List
from tabletlib.graphics.rectangle_se import RectangleSE

if TYPE_CHECKING:
    from tabletlib.layer import Layer

logger = logging.getLogger(__name__)

tbox_xoffset = 4  # QT distance from text item origin (setPos) to lower left corner of text bounding box
tbox_yoffset = 4  # For now, determined experimentally, not sure how to compute it from QFontMetrics

underlay_margin_h = 5  # Horizontal and vertical distances from text to outer edge of underlay
underlay_margin_v = 5

underlay_offset_x = 2  # Lower left corner offsets from lower left origin of text item origin
underlay_offset_y = 3

Qt_font_weight = {'normal': QFont.Weight.Normal, 'bold': QFont.Weight.Bold}
"""Maps an application style to a Qt specific font weight"""


class TextElement:
    """
    Manage the rendering of Text Elements
    """
    @classmethod
    def line_size(cls, layer: 'Layer', asset: str, text_line: str) -> Rect_Size:
        """
        Returns the size of a line of text when rendered with the asset's text style

        :param layer: Text is drawn on this Layer
        :param asset: Application entity to determine text style
        :param text_line: Text that would be rendered
        :return: Size of the text line ink area
        """
        style_name = layer.Presentation.Text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_name = StyleDB.typeface[style.typeface]

        font = QFont(font_name, style.size)
        font.setItalic(style.slant == 'italic')
        font.setBold(style.weight == 'bold')

        font_metrics = QFontMetrics(font)
        bound_rect = font_metrics.boundingRect(text_line)

        # Comments below are from Cairo implementation
        # Keeping them for now in case they become relevant
        # # te = self.Tablet.Context.text_extents(text_line)
        # # Add x_bearing to account for any indented whitespace
        # # Otherwise you just get the width of the text after the whitespace
        # return Rect_Size(height=te.height, width=te.width+te.x_bearing)

        return Rect_Size(height=bound_rect.height(), width=bound_rect.width())

    @classmethod
    def text_block_size(cls, layer: 'Layer', asset: str, text_block: List[str]) -> Rect_Size:
        """
        Determines the dimensions of a rectangle bounding the text to be drawn.

        :param layer: Text in block is drawn on this layer
        :param asset: Name of the text asset to get display style properties
        :param text_block: A list of text lines to be displayed
        :return:  The display size of the text bloxk
        """
        style_name = layer.Presentation.Text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_height = style.size
        spacing = font_height*style.spacing
        inter_line_spacing = spacing - font_height  # Space between two lines

        num_lines = len(text_block)
        assert num_lines > 0, "Text block size requested for empty text block"
        # The text block is the width of its widest ink render extent
        widths = [cls.line_size(layer=layer, asset=asset, text_line=line).width for line in text_block]
        widest_line = text_block[widths.index(max(widths))]
        block_width = cls.line_size(layer=layer, asset=asset, text_line=widest_line).width
        block_height = num_lines*spacing - inter_line_spacing  # Deduct that one unneeded line of spacing on the top

        return Rect_Size(width=block_width, height=block_height)

    @classmethod
    def add_underlay(cls, layer: 'Layer', lower_left: Position, size: Rect_Size):
        """
        Adds a rectangle matching the color of the sheet layer (if one exists) otherwise, defaults
        to white. This rectangle will be drawn underneath a text line or block so that the color surrounding
        the text matches the background color. This is useful when you want to draw text over the top of some
        graphical component such as a line without being too visually disruptive.
        """
        # Use the scene background or white if no background is specified
        fill = (255, 255, 255) if not layer.Tablet.background_color else layer.Tablet.background_color

        # Flip lower left corner to device coordinates
        ll_dc = layer.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        layer.TextUnderlayRects.append(element.FillRect(upper_left=ul, size=size, color=fill))

    @classmethod
    def add_line(cls, layer: 'Layer', asset: str, lower_left: Position, text: str):
        """
        Adds a line of text to the Tablet at the specified lower left corner location which will be converted
        to device coordinates
        """
        # Qt positions using the upper left corner
        # We need to determine the height of the text bounding box to determine the upper left corner
        ll_dc = layer.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))  # Convert to device coordinates
        tl_size = cls.line_size(layer=layer, asset=asset, text_line=text)  # Get height of bounding box
        # Compute upper left corner using experimentally observed offset
        ul = Position(x=ll_dc.x-tbox_xoffset, y=ll_dc.y - tl_size.height - tbox_yoffset)

        if asset in layer.Presentation.Underlays:
            # Compute a rectangle slightly larger than the text area to underlay the text
            underlay_size = Rect_Size(height=tl_size.height+underlay_margin_v, width=tl_size.width+underlay_margin_h)
            underlay_pos = Position(lower_left.x-underlay_offset_x, lower_left.y-underlay_offset_y)
            cls.add_underlay(layer=layer, lower_left=underlay_pos, size=underlay_size)
        try:
            layer.Text.append(
                element.Text_line(
                    upper_left=ul, text=text,
                    style=layer.Presentation.Text_presentation[asset],
                )
            )
        except TabletBoundsExceeded:
            logger.warning(f"Asset: [{asset}] Text: [{text}] outside of tabletlib draw area")
            return


    @classmethod
    def add_block(cls, layer: 'Layer', asset: str, lower_left: Position, text: List[str],
                       align: HorizAlign = HorizAlign.LEFT):
        """
        Add all lines in this block of text to the Tablet.

        Set the lower left x of each line based on right or left alignment
        within the text block.  Assuming left alignment as default.

        :param layer:  Add text to this Layer
        :param asset:  To get the text style
        :param lower_left: Lower left corner of the text block on the Tablet
        :param text: One or more lines of text
        :param align: Horizontal text alignment (left, right or center)
        """
        style_name = layer.Presentation.Text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_height = style.size
        spacing = font_height*style.spacing

        # Get height of one line (any will do since they all use the same text style)
        xpos, ypos = lower_left  # Initialize at lower left corner
        x_indent = 0  # Assumption for left aligned block
        block_width = None
        if align != HorizAlign.LEFT:
            # We'll need the total width of the block as a reference point
            longest_line = max(text, key=len)
            block_width = cls.line_size(layer=layer, asset=asset, text_line=longest_line).width
        for line in text[::-1]:  # Reverse order since we are positioning lines from the bottom up
            # always zero indent from xpos when left aligned
            if align == HorizAlign.RIGHT:
                assert block_width, "block_width not set"
                line_width = cls.line_size(layer=layer, asset=asset, text_line=line).width
                x_indent = block_width - line_width  # indent past xpos by the difference
            if align == HorizAlign.CENTER:
                line_width = cls.line_size(layer=layer, asset=asset, text_line=line).width
                x_indent = (block_width - line_width) / 2  # indent 1/2 of non text span
            cls.add_line(layer=layer, asset=asset, lower_left=Position(xpos+x_indent, ypos), text=line)
            ypos += spacing

    @classmethod
    def render_underlays(cls, layer: 'Layer'):
        """
        Draw all text underlays as filled, borderless rectangles

        :param layer: Draw on this layer
        """
        for u in layer.TextUnderlayRects:
            RectangleSE.render_fillrect(layer=layer, frect=u)

    @classmethod
    def render(cls, layer: 'Layer'):
        """Draw all text lines"""
        for t in layer.Text:
            t_item = QGraphicsTextItem(t.text)
            style = StyleDB.text_style[t.style]
            text_color_name = StyleDB.text_style[t.style].color
            text_rgb_color_value = StyleDB.rgbF[text_color_name]
            t_item.setDefaultTextColor(QColor(*text_rgb_color_value))
            font = QFont(StyleDB.typeface[style.typeface], style.size)
            font.setWeight(Qt_font_weight[style.weight])
            if style.slant == 'italic':
                font.setItalic(True)
            t_item.setFont(font)
            logger.info(f'Font [{style}]')
            t_item.setPos(t.upper_left.x, t.upper_left.y)
            logger.info(f'> Text line [{t.text}] at {t.upper_left}')
            layer.Scene.addItem(t_item)
