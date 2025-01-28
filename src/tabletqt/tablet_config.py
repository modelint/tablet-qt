""" tablet_config.py -- Configuration class from Render Subsystem class model """

# System
from pathlib import Path

class TabletConfig:
    """

    """
    config_path = Path(__file__).parent / "configuration"
    image_path = config_path / "images"
    app_name = "mi_tablet"
