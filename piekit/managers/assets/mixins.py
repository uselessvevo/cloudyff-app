import typing
from typing import Union

from PySide6.QtGui import QIcon

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class AssetsAccessor:
    """
    Config mixin
    """

    def get_asset(
        self,
        key: typing.Any,
        default: typing.Any = None,
        section: Union[str, Section] = Section.Shared
    ) -> typing.Any:
        return Managers(SysManager.Assets).get(self.section or section, key, default)

    def get_asset_icon(
        self,
        key: typing.Any,
        default: typing.Any = None,
        section: Union[str, Section] = Section.Shared
    ):
        return QIcon(Managers(SysManager.Assets).get(self.section or section, key, default))

    def get_plugin_icon(self) -> "QIcon":
        return QIcon(Managers(SysManager.Assets).get(self.name, "app.png"))

    getAsset = get_asset
    getAssetIcon = get_asset_icon
    getPluginIcon = get_plugin_icon
