"""
presentation.py – Presentation class in View domain
"""
import logging
from collections import namedtuple
import yaml
from pathlib import Path


CornerSpec = namedtuple('Corner_Spec', 'radius top bottom')
config_dir = Path(__file__).parent / "config"


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
        file_path = config_dir / "drawing_types.yaml"
        self.logger.info(f"loading assets in: [{file_path}]")
        with open(file_path, 'r') as file:
            raw_data = yaml.safe_load(file)
        my_data = raw_data[self.Drawing_type][self.Name]
        # Load text presentations
        for asset_name,v in my_data['text'].items():
            self.Text_presentation[asset_name] = v['Text style']
            if v['Underlay']:
                self.Underlays.add(asset_name)
        # Load shape presentations
        for asset_name, v in my_data['shape'].items():
            self.Shape_presentation[asset_name] = v['Line style']
            fill = v.get('Fill')
            if fill:
                self.Closed_shape_fill[asset_name] = fill
            corner_spec = v.get('Corner spec')
            if corner_spec:
                self.Corner_spec[asset_name] = CornerSpec(radius=corner_spec['Radius'], top=corner_spec['Top'],
                                                          bottom=corner_spec['Bottom'])
