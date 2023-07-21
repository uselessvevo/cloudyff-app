import os

from piekit.config.types import Lock
from piekit.managers.structs import DirectoryType
from piekit.managers.structs import ManagerConfig


# Application main info
PIEAPP_NAME: Lock = "pie-audio"
PIEAPP_VERSION: Lock = "1.0.0"
PIEAPP_PROCESS_NAME_ID = "com.crabdevs.pieaudio"
PIEAPP_PROJECT_URL = "https://github.com/uselessvevo/pie-audio/"

MAIN_WINDOW_MIN_WINDOW_SIZE: Lock = (720, 480)

# List of excluded file formats
ASSETS_EXCLUDED_FORMATS = [DirectoryType, ".qss", ".json", ".ttf", ".py"]

DEFAULT_CONFIG_FILES = [
    "locales.json",
    "assets.json",
    "ffmpeg.json",
]

USE_TEST_PLUGIN = os.getenv("PIE_USE_TEST_PLUGIN", True)

# Managers startup configuration
INITIAL_MANAGERS: Lock = [
    ManagerConfig(
        import_string="piekit.managers.configs.manager.ConfigManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.locales.manager.LocaleManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.assets.manager.AssetsManager",
        init=True
    ),
]

MANAGERS: Lock = [
    *INITIAL_MANAGERS,
    ManagerConfig(
        import_string="piekit.managers.menus.manager.MenuManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.toolbars.manager.ToolBarManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.toolbuttons.manager.ToolButtonManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.confpages.manager.ConfigPageManager",
        init=True
    ),
    ManagerConfig(
        import_string="piekit.managers.plugins.manager.PluginManager",
        init=True
    ),
]
