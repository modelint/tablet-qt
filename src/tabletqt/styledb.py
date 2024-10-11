"""
styledb.py - Loads styles common to all Presentations
"""
import logging
from pathlib import Path
from typing import NamedTuple, Any
from mi_config.config import Config
from tabletqt.configuration.styles import (ColorCanvas, FloatRGB, LineStyle,
                                           TextStyle, DashPattern)

_logger = logging.getLogger(__name__)


config_dir = Path(__file__).parent / "configuration"
# nt - named tuple is defined
# pre/post - Whether or not the data must be pre or post processed
# PP = namedtuple('PP', 'nt pre post')  # Postprocess configuration file data

class PP(NamedTuple):
    nt: Any
    pre: bool
    post: bool


# yaml file name : load data using this tuple
config_type = {
    'colors': PP(nt=ColorCanvas, pre=True, post=False),
    'line_styles': PP(nt=LineStyle, pre=False, post=False ),
    'dash_patterns': PP(nt=DashPattern, pre=False, post=False),
    'typefaces': PP(nt=None, pre=False, post=False),
    'text_styles': PP(nt=TextStyle, pre=False, post=True),
    'color_usages': PP(nt=None, pre=False, post=True)
}


class StyleDB:
    """
    Manages a set of graphic and text styles defined for the Drawing Types that will be used
    with a Tablet. The client app can then refer to these styles rather than explicitly specifying
    graphics properties like font, line width, color fill and so forth.

    For example, the client app might request a 'state activity compartment' and then obtain
    all the predefined styles automatically.

    The styles are all defined in a set of yaml files that reference each other's
    elements.
    """
    styles = {}  # { 'text_style':
    rgbF = {}  # rgb color float representation
    typeface = None
    dash_pattern = None
    line_style = None
    text_style = None
    color_usage = None

    def __init__(self):
        """
        Initialize a Style DB
        """
        fspecs = {k: v.nt for k,v in config_type}
        c = Config(app_name='tablet', lib_config_dir=config_dir, fspecs=fspecs)



    @classmethod
    def load_config_files(cls):
        """
        Processes the config_type dictionary, loading each yaml configuration file into either
        a named tuple or a simple key value dictionary if no named tuple is provided
        and then sets the corresponding StyleDB class attribute to that value
        """
        _logger.info(f"StyleDB loading tabletqt configuration\n---")
        cf_dict = Config.load()
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
                          f"text styles configuration file:\n    {config_dir / 'text_styles.yaml'}")
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
                                  f"configuration file:\n    {config_dir / 'colors.yaml'}")
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
                          f"color usages configuration file:\n    {config_dir / 'color_usages.yaml'}")
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
