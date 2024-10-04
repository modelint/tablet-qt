"""
styledb.py - Loads styles common to all Presentations
"""
import logging
from pathlib import Path
import yaml
from collections import namedtuple
from tabletqt.exceptions import BadConfigData

_logger = logging.getLogger(__name__)

Color_Canvas = namedtuple('Color_Canvas', 'r g b canvas')
Float_RGB = namedtuple('Float_RGB', 'r g b')
Line_Style = namedtuple('Line_Style', 'pattern width color')
Text_Style = namedtuple('Text_Style', 'typeface size slant weight color spacing')
Dash_Pattern = namedtuple('Dash_Pattern', 'solid blank')

config_dir = Path(__file__).parent / "config"
# nt - named tuple is defined
# pre/post - Whether or not the data must be pre or post processed
PP = namedtuple('PP', 'nt pre post')  # Postprocess config file data

# yaml file name : load data using this tuple
config_type = {
    'colors': PP(Color_Canvas, pre=True, post=False),
    'line_styles': PP(nt=Line_Style, pre=False, post=False ),
    'dash_patterns': PP(nt=Dash_Pattern, pre=False, post=False),
    'typefaces': PP(nt=None, pre=False, post=False),
    'text_styles': PP(Text_Style, pre=False, post=True),
    'color_usages': PP(nt=None, pre=None, post=True)
}


def load_yaml_to_namedtuple(file_path, namedtuple_type):
    with open(file_path, 'r') as file:
        raw_data = yaml.safe_load(file)
    if not isinstance(raw_data, dict):
        raise BadConfigData(f"Expected dict when loading:\n    {file_path}")
    return {k: namedtuple_type(**v) for k, v in raw_data.items()}


class StyleDB:
    """
    Singleton class interface to the Presentation and Styles in the Flatland database. Created with an initial
    Presentation and loads all presentation/style data for that Presentation for easy access by
    the Tablet.
    """
    styles = {}  # { 'text_style':
    rgbF = {}  # rgb color float representation
    typeface = None
    dash_pattern = None
    line_style = None
    text_style = None
    color_usage = None

    @classmethod
    def load_config_files(cls):
        """
        Processes the config_type dictionary, loading each yaml config file into either
        a named tuple or a simple key value dictionary if no named tuple is provided
        and then sets the corresponding StyleDB class attribute to that value
        """
        _logger.info(f"StyleDB loading tabletqt configuration\n---")
        for fname, pp in config_type.items():
            config_file_path = config_dir / (fname+".yaml")
            _logger.info(f"loading: {config_file_path}")
            if pp.nt:
                # A named tuple is defined for this file, so we use it to load the data
                attr_val = load_yaml_to_namedtuple(config_file_path, pp.nt)
            else:
                # No named tuple, so we just read file into a dictionary
                with open(config_file_path, 'r') as file:
                    attr_val = yaml.safe_load(file)
            if pp.pre:
                # Retrieve the relevant preprocessing method name using the filename suffix
                method_name = 'preprocess_'+fname
                method = getattr(cls, method_name, None)
                # Invoke it on the loaded yaml data
                method(attr_val)
            attr_name = fname[:-1]  # drop the plural 's' from the file name to get the attribute name
            # Assign the loaded and possibly preprocessed yaml data to the relevant class attribute
            setattr(cls, attr_name, attr_val)
            if pp.post:
                method_name = 'postprocess_'+fname  # Keep the plural
                method = getattr(cls, method_name, None)
                method()

        _logger.info(f"---\n")

    @classmethod
    def postprocess_text_styles(cls):
        """
        Verify all typefaces are defined
        """
        undefined_typefaces = [t.typeface for t in cls.text_style.values() if t.typeface not in cls.typeface]
        if undefined_typefaces:
            _logger.error(f"Undefined typefaces: {undefined_typefaces} encountered in"
                          f"text styles config file:\n    {config_dir / 'text_styles.yaml'}")
            raise BadConfigData


    @classmethod
    def preprocess_colors(cls, raw_data):
        """
        # Validate color float values for QT6
        """
        for name, rgb in raw_data.items():
            for n in [rgb.r, rgb.g, rgb.b]:
                if not 0 <= n <= 255:
                    _logger.error(f"Bad color value [{n}] for: {name} in "
                                  f"config file:\n    {config_dir / 'colors.yaml'}")
                    raise BadConfigData
            StyleDB.rgbF[name] = Float_RGB(r=rgb.r, g=rgb.g, b=rgb.b)

    @classmethod
    def postprocess_color_usages(cls):
        """
        Validate color names
        """
        undefined_colors = [c for c in cls.color_usage.values() if c not in cls.rgbF]
        if undefined_colors:
            _logger.error(f"Undefined colors: {undefined_colors} encountered in"
                          f"color usages config file:\n    {config_dir / 'color_usages.yaml'}")
            raise BadConfigData

    @classmethod
    def report_colors(cls):
        """
        Prints out a list of the available colors for the user
        """
        cls.load_config_files()
        print("Canvas colors:")
        print("---")
        for c in cls.rgbF:
            print(c)
        print("===")
