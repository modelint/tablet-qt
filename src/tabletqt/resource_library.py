""" resource.py -- Manage user resources, image files for now """

# Tablet
from tabletqt.tablet_config import TabletConfig

# System
import shutil
from pathlib import Path

class ResourceLibrary:

    system_image_path = Path(__file__).parent / 'configuration/image_files'

    @classmethod
    def init_user_images(cls):
        """
        Copy user startup image files to their .config/mi_tablet/configuration/images dir
        Create that directory if it doesn't yet exist
        """
        user_image_path = Path.home() / ".config" / TabletConfig.app_name / "images"
        user_image_path.mkdir(parents=True, exist_ok=True)
        for f in cls.system_image_path.iterdir():
            if not (user_image_path / f.name).exists():
                shutil.copy(src=f, dst=user_image_path)
