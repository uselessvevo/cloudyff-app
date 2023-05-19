from typing import Union, Type
from pathlib import Path

from piekit.utils.logger import logger
from piekit.utils.files import read_json
from piekit.utils.modules import import_by_string
from piekit.managers.base import BaseManager
from piekit.managers.structs import ManagerConfig


class ManagersRegistry:

    def __init__(self) -> None:
        # Just a logger
        self._logger = logger

        # Dictionary with stored `BaseManager` base classes. Use to reload them
        self._managers_instances: dict[str, BaseManager] = {}

    def from_class(self, manager_class: Type[BaseManager], init: bool = True, *args, **kwargs) -> None:
        """
        Initialize manager manualy. Pass manager class (not an instance) with args and kwargs
        For example:
        >>> from piekit.managers.registry import Managers
        >>> from piekit.managers.configs.manager import ConfigManager
        >>> Managers.init(ConfigManager, PathConfig(...), ...)
        """
        manager_instance = manager_class()
        self._logger.info(f"Initializing `{manager_instance.__class__.__name__}`")

        if init is True:
            manager_instance.init(*args, **kwargs)

        self._managers_instances[manager_instance.name] = manager_instance
        setattr(self, manager_instance.name, manager_instance)
        setattr(manager_instance, "ready", init)

    def from_config(self, config: ManagerConfig) -> None:
        """
        Initialize manager from `ManagerConfig` structure
        """
        manager_instance = import_by_string(config.import_string)()
        self._logger.info(f"Initializing `{manager_instance.__class__.__name__}`")

        if config.init is True:
            manager_instance.init(*config.args, **config.kwargs)

        self._managers_instances[manager_instance.name] = manager_instance
        setattr(self, manager_instance.name, manager_instance)
        setattr(manager_instance, "ready", config.init)

    def from_json(self, file: Union[str, Path]) -> None:
        """
        Initialize managers from json file.
        File structure must have an array with the next parameters
            * import_string (str): import string separated by dots - 'path.to.manager.ManagerClassName'
            * init (bool): initialize manager

        For example: `[{"import_string": string, "init": boolean}, ...]`
        """
        file_data = read_json(file)
        file_data = tuple(ManagerConfig(import_string=f["import"], init=file["init"]) for f in file_data)

        for config in file_data:
            self.from_config(config)

    def shutdown(self, *managers: str, full_house: bool = False) -> None:
        self._logger.info("Preparing to shutdown all managers")
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = (self._managers_instances.get(i) for i in managers or self._managers_instances.keys())

        for manager_instance in managers_instances:
            self._logger.info(f"Shutting down `{manager_instance.__class__.__name__}` from `{self.__class__.__name__}`")
            manager_name = manager_instance.name
            manager_instance.shutdown(full_house=True)
            delattr(self, manager_name)

    def reload(self, *managers: tuple[BaseManager], full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers
        managers_instances = (self._managers_instances.get(i) for i in managers)

        for manager_instance in managers_instances:
            self._logger.info(f"Reloading `{manager_instance.__class__.__name__}`")
            manager_instance.reload()

    def destroy(self, *managers: str, full_house: bool = False):
        managers = reversed(self._managers_instances.keys()) if full_house else managers

        for manager in managers:
            self._logger.info(f"Destroying `{manager.__class__.__name__}`")
            delattr(self, manager)

    def __call__(self, manager: str) -> BaseManager:
        try:
            return self.__getattribute__(manager)
        except AttributeError:
            raise AttributeError(f"Manager `{manager}` not found or not initialized")


Managers = ManagersRegistry()