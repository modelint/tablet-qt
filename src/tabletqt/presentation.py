"""
presentation.py – Presentation class in View domain
"""
# System
import logging
from collections import namedtuple
from pathlib import Path

# Modelint
from mi_config.config import Config

CornerSpec = namedtuple('Corner_Spec', 'radius top bottom')
config_dir = Path(__file__).parent / "configuration"

_logger = logging.getLogger(__name__)


class Presentation:
    """
   A set of compatible visual styles including fonts, colors, border widths and so forth as appropriate to a
   given View Type form a selectable Presentation. For example, an `Executable UML State Machine Diagram`
   might be drawn using certain fonts for state stickers and possibly different colors for transient and
   non-transient states. Alternatively, only black and white might be used with purple for a certain kind of
   connector in a diagnostic Presentation.
   """

    def __init__(self, name: str, drawing_type: str):
        """
       Constructor
       """
        self.logger = logging.getLogger(__name__)
        self.Name = name
        self.Drawing_type = drawing_type
        self.Text_presentation = {}
        self.Underlays = set()  # Set of text presentations that require an underlay
        self.Line_presentation = {}
        self.Rectangle_presentation = {}
        self.Symbol_presentation = {}
        self.Corner_spec = {}

        # Load Asset Presentations for all Assets in this Presentation
        self.logger.info(f"using presentation: [{self.Name}]")
        self.load_drawing_type()

    def load_drawing_type(self):
        """
        Load symbol, shape, and text assets for my drawing type and presentation
        """
        _logger.info(f"Loading presentations\n---")

        c = Config(app_name='mi_tablet', lib_config_dir=config_dir, fspec={'drawing_types':None})
        dtype_data = c.loaded_data['drawing_types']
        try:
            my_data = dtype_data[self.Drawing_type][self.Name]
        except KeyError:
            _logger.error(f"No presentation [{self.Name}] defined for drawing type [{self.Drawing_type}]")
            raise

        # Load symbol presentations
        self.Symbol_presentation = my_data.get('symbol')
        self.Text_presentation = my_data.get('text')
        if my_data.get('shape'):
            self.Rectangle_presentation = my_data['shape'].get('rectangle')
            self.Line_presentation = my_data['shape'].get('line')