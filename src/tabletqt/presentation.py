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
   might be drawn using certain fonts for state names and possibly different colors for transient and
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
        self.Shape_presentation = {}
        self.Closed_shape_fill = {}
        self.Corner_spec = {}

        # Load Asset Presentations for all Assets in this Presentation
        self.logger.info(f"using presentation: [{self.Name}]")
        self.load_drawing_type()

    def load_drawing_type(self):
        """
        Load shape and text assets for my drawing type and presentation
        """
        _logger.info(f"Loading presentations\n---")

        c = Config(app_name='mi_tablet', lib_config_dir=config_dir, fspec={'drawing_types':None})
        dtype_data = c.loaded_data['drawing_types']
        try:
            my_data = dtype_data[self.Drawing_type][self.Name]
        except KeyError:
            _logger.error(f"No presentation [{self.Name}] defined for drawing type [{self.Drawing_type}]")
            raise

        # Load text presentations
        for asset_name, v in my_data['text'].items():
            self.Text_presentation[asset_name] = v['text style']
            if v['underlay']:
                self.Underlays.add(asset_name)
        # Load shape presentations
        for asset_name, v in my_data['shape'].items():
            self.Shape_presentation[asset_name] = v['line style']
            fill = v.get('fill')
            if fill:
                self.Closed_shape_fill[asset_name] = fill
            corner_spec = v.get('corner spec')
            if corner_spec:
                self.Corner_spec[asset_name] = CornerSpec(radius=corner_spec['radius'], top=corner_spec['top'],
                                                          bottom=corner_spec['bottom'])
