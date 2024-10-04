"""
tabletqt.py – A multi-layered drawing surface implemented on top of the Qt GUI framework
"""
# System
import sys  # For fatal error exit
import logging
from datetime import datetime  # For initial log entry
from pathlib import Path
from typing import Optional

# Qt
from PyQt6.QtWidgets import QApplication

# Tablet
from tabletqt.exceptions import NonSystemInitialLayer, TabletBoundsExceeded
from tabletqt.geometry_types import Rect_Size, Position
from tabletqt.styledb import StyleDB
from tabletqt.layer import Layer
from tabletqt.scene_view import MainWindow
from tabletqt.styledb import Float_RGB

default_background = Float_RGB(255, 255, 255)  # White

class Tablet:
    """
    The Tablet class is part of the Drawing domain which provides a service to an application
    with simple 2D diagramming needs such as the Flatland model diagram generator.

    Most importantly, the Drawing domain and hence the Tablet abstract away the details of
    graphics library interaction from the fundamental diagramming application.

    The original implementation of Tablet supported the Cairo graphics library while the current
    implementation is built on the Qt Gui framework. No changes are necessary in any client diagramming
    applications that draw on a Tablet.

    For example, when a Flatland node compartment wants to draw itself, it doesn't worry about line
    widths, dash patterns and colors. It also doesn't worry about flipping to whatever coordinate
    system the graphics library uses. A compartment would just say "add_shape( asset, size, location )" and
    the Tablet will take care of the rest. Here the asset is the name of the model entity 'compartment',
    the size in points (or whatever units the Flatland app wants to use) and location expressed in Flatland
    Canvas coordinates.

    When a Tablet is created, it is initialized with a single populated Layer where Assets can be drawn.
    For example, Flatland might start with a predefined 'diagram' Layer using a Drawing Type such as
    'state machine diagram' and a Presentation such as 'default' or 'formal' or 'corporate'.

    The Diagram Type determines what kinds of things might be drawn, Assets such as 'connector',
    'compartment', 'class name', etc., while the Presentation establishes the Text and Line Styles to
    be used when drawing those Assets. All of this information is stored in yaml files which the Tablet
    loads upon creation.

    Each time the application wants something drawn, it will ask Tablet to add the appropriate Asset
    to one of its render lists. A separate list is maintained for all the rectangles, line segments and
    text lines to be rendered. When the application is finished populating these lists, the Tablet can
    render everything using its graphic library (Qt in this implementation) using whatever coordinate
    system the library supplies, making any necessary conversions from the application coordinate system.

        Attributes and relationships defined on the class model

        - ID {I} -- Unique id, implemented as a reference to a Tablet object, no attribute needed
        - Size -- The height and width of the drawing surface (attribute)
        - Output_file -- A filename or output stream object to be output as a drawing (attribute)
        - Background_color -- The color of the Tablet (visible through all non-opaque layer elements)
    """

    def __init__(self, size: Rect_Size, output_file: Path, drawing_type: str, presentation: str,
                 layer: str, background_color: Float_RGB = default_background):
        """
        Constructs a new Tablet instance with a single initial predefined Layer

        :param size: Vertical and horizontal span of the entire draw surface in points
        :param output_file: Name of the drawing file to be generated, PDF only for now
        :param drawing_type: Initial layer Drawing Type so we know what kinds text and graphics Assets can be drawn
        :param presentation: Initial layer's Presentation so we know what graphic styles to use for our Assets
        :param layer: The name of the predefined initial Layer to be created on this Tablet (typically 'diagram')
        :param background_color: RGB tabletqt background color, set to white if none specified
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Tablet init: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Load all of the common font, color, etc. styles used by all Presentations from yaml files
        StyleDB.load_config_files()

        # Establish a system default layer ordering. Not all of them will be used in any given
        # View, but this is the draw order from bottom-most layer upward
        # It can (should be) customizable by the user, but this should work for most diagrams
        self.background_color = background_color  # This is referenced when filling text underlay rects
        self.layer_order = ['sheet', 'grid', 'frame', 'diagram', 'scenario', 'annotation']
        self.Presentations = {}  # Presentations loaded from the Flatland database, updated by Layer class
        self.App = QApplication([])  # QT Application (must be created before any QT widgets)
        self.Window = MainWindow("Tablet", size, self.background_color)  # QT widget for drawing 2D elements
        self.View = self.Window.graphics_view

        if layer not in self.layer_order:
            raise NonSystemInitialLayer
        self.layers = {layer: Layer(name=layer, tablet=self, presentation=presentation, drawing_type=drawing_type)}
        # Initialize the first layer at the indicated position. If the position is not in the system layer order
        # list, it will be placed as the topmost layer. Usually, though, the initial layer should be diagram

        # self.Drawing_type = drawing_type  # class diagram, state diagram, etc
        self.Size = size
        self.Output_file = output_file

    def add_layer(self, name: str, presentation: str, drawing_type: str) -> Optional[Layer]:
        """
        Populate a new layer by name and return it. If a layer of the same name has already been
        populated, no layer is returned.

        All drawing takes place on a designated layer, such as 'diagram' or 'sheet'.

        A defined layer is simply a known layer name within a predefined rendering order.
        You can think of each position in the order as a z coordinate with 0 corresponding to the first
        rendered layer. For example, the 'sheet' layer is at the bottom (0) with 'diagram' somewhere
        above it.

        A layer, predefined or custom, must be populated before anything can be drawn on it.
        The client application is responsible for populating any layers that it needs. There is not automatic
        population.

        If a layer name is supplied that does not correspond to any of the predefined layers, it will be stacked
        after the last predefined layer and, thus, rendered last.

        :param name: One of the standard layer names or a custom layer name
        :param presentation: The Presentation name associated with this Layer
        :param drawing_type: The Drawing Type defining this Presentation
        :return: A reference to the newly created layer
        """
        if not self.layers.get(name):
            if name not in self.layer_order:
                self.layer_order.append(name)
            self.layers[name] = Layer(name=name, tablet=self, presentation=presentation, drawing_type=drawing_type)
            return self.layers[name]
        else:
            self.logger.warning(f"Layer: [{name}] already exists")
            return None

    def render(self):
        """
        Renders each populated layer of the Tablet moving up the z axis. Any unpopulated layers are skipped.
        """
        # Create and show the drawing window
        [self.layers[name].render() for name in self.layer_order if self.layers.get(name)]
        self.Window.show()

        # Save the rendered tabletqt as a PDF for alternate viewing
        self.View.save_as_pdf(self.Output_file)

        # Run the Qt GUI event loop
        sys.exit(self.App.exec())

    def to_dc(self, tablet_coord: Position) -> Position:
        """
        Convert from tabletqt coordinates (tc) used by the client application to device
        coordinates (dc).

        Tablet coordinates are upper right quadrant cartesian with the origin (0,0) in the
        lower left corner of the tabletqt. This is what client application (user) specifies
        when drawing.

        Device coordinates depend on the graphics library. Here we are using Qt, so we have
        a standard display coordinate system with the origin in the upper left corner with
        y values ascending toward the bottom of the display.

        An exception is thrown if the supplied position is outside of the tabletqt boundary.

        Note: This may seem like overkill for a simple computation and check, but less
        error prone than having this pattern sprinked throughout the code.

        :param tablet_coord: Position in table coordinates
        :return: Position in device coordinates
        """
        if tablet_coord.y > self.Size.height:
            raise TabletBoundsExceeded
        assert tablet_coord.x >= 0, "Negative x value"
        assert tablet_coord.y >= 0, "Negative y value"
        return Position(x=tablet_coord.x, y=self.Size.height - tablet_coord.y)

    def __repr__(self):
        return f'Size: {self.Size},  Output: {self.Output_file}'
