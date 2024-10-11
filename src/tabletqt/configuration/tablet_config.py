""" tablet_config.py - Manage loading and creation of user configuration files """

# System
import logging
import shutil
from pathlib import Path

_logger = logging.getLogger(__name__)


class TabletConfig:

    config_dir_file_name = ".mi_tablet"

    @classmethod
    def load(cls):
        """
        Load all config files from the user config directory

        """
        pass

    @classmethod
    def setup(cls):
        """
        Verify that the config files exist in the user's home config directory.
        If the directory does not exist, or any of the files are missing, do a reset
        """
        print()
        pass




    @classmethod
    def reset(cls):
        """
        Copy user startup configuration files to their .mi_tablet/configuration dir
        Create that directory if it doesn't yet exist
        """
        user_config_path = Path.home() / cls.config_dir_file_name
        user_config_path.mkdir(parents=True, exist_ok=True)
        system_config_path = Path(__file__).parent / 'configuration'
        for f in system_config_path.iterdir():
            if not (user_config_path / f.name).exists():
                shutil.copy(f, user_config_path)
