from typing import Union
from pathlib import Path

from PySide6.QtCore import Signal, QObject

from piekit.config import Config
from piekit.utils.logger import logger
from piekit.managers.base import BaseManager
from piekit.plugins.types import PluginTypes, Error
from piekit.plugins.observer import PluginsObserverMixin


class PiePlugin(
    QObject,
    PluginsObserverMixin,
):
    # Main attributes #

    # Plugin type
    type: PluginTypes = PluginTypes.Plugin

    # Icon name
    icon: Union[None, str] = Config.PLUGIN_ICON_NAME

    # By default, description must be written in English
    description: str = None

    # Plugin codename
    name: str

    # Accessors section
    section: str = None

    # PiePlugin version
    version: str = None
    pieapp_version: str = None
    piekit_version: str = None

    # List of required built-in plugins
    requires: list[str] = []

    # List of optional built-in plugins
    optional: list[str] = []

    api: "PiePluginAPI" = None

    # Qt configuration #

    # Signal when plugin is ready
    sig_plugin_ready = Signal()

    # Signal when plugin is loading
    sig_plugin_loading = Signal(str)

    # Signal when plugin is reloading
    sig_plugin_reloading = Signal(str)

    # Signal when main window is closing
    sig_on_main_window_close = Signal()

    # Signal when exception occurred
    sig_exception_occurred = Signal(Error)

    def __init__(
        self,
        parent: "QMainWindow" = None,
        path: Path = None,
    ) -> None:
        # For some reason, I can't use `super().__init__()` method with `PySide`

        # Initialize `QObject` instance
        QObject.__init__(self, parent)

        # Initialize `PluginsObserverMixin` instance
        PluginsObserverMixin.__init__(self)

        # Just a logger
        self._logger = logger

        # Parent object/window
        self._parent = parent

        # PiePlugin path
        self._path: Path = path

        self._managers: list[BaseManager] = []

    # Prepare methods

    def prepare(self) -> None:
        # First, we need to initialize base signals
        self.prepare_base_signals()

        # PiePlugin is loading
        self.sig_plugin_loading.emit(self.__class__.__name__)

        # Initializing plugin
        self.init()

        # Prepare PiePluginAPI
        self.init_api()

    # Signals, shortcuts etc. methods

    def prepare_base_signals(self):
        self.logger.info(f"Preparing base signals for {self.__class__.__name__}")
        self.sig_plugin_loading.connect(self._parent.sig_plugin_loading)
        self.sig_plugin_reloading.connect(self._parent.sig_plugin_reloading)
        self.sig_exception_occurred.connect(self._parent.error_handler)

    # Main methods

    def init(self) -> None:
        """
        Initialize an object for the first time.
        For example, you can call managers' register method
        """

    def call(self) -> None:
        """
        Call an object.
        Notice, don't call managers' register methods.
        """
        raise NotImplementedError(f"Method `call` is not implemented")

    def init_api(self) -> None:
        """
        Method that prepare PiePluginAPI based instance
        """
        from piekit.plugins.api.api import PiePluginAPI

        if self.api and issubclass(self.api, PiePluginAPI):
            self.api = self.api(self)
            self.api.init()

    # Getter methods

    def get_description(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"

    def get_name(self) -> str:
        return self.name or self.__class__.__name__

    def get_version(self) -> str:
        return self.version

    # Properties

    @property
    def logger(self):
        return self._logger

    @property
    def path(self) -> Path:
        return self._path
