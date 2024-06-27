from PySide6.QtWidgets import QDialog, QGridLayout

from pieapp.api.models.workbench import WorkbenchItem
from pieapp.api.plugins import PiePlugin
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_ready

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.toolbuttons.mixins import ToolButtonAccessorMixin


class History(PiePlugin, ThemeAccessorMixin, ToolButtonAccessorMixin):
    name = SysPlugin.Appearance
    requires = [SysPlugin.Preferences, SysPlugin.MainToolBar]

    def init(self) -> None:
        self._history_dialog = QDialog()
        self._main_grid_layout = QGridLayout()
        self._history_dialog.set_layout(self._main_grid_layout)

    @on_plugin_ready(plugin=SysPlugin.MainToolBar)
    def _on_main_toolbar_available(self) -> None:
        main_toolbar = get_plugin(SysPlugin.MainToolBar)
        history_tool_button = self.add_tool_button(
            scope=self.name,
            name=WorkbenchItem.History,
            text=translate("History"),
            tooltip=translate("Show files history"),
            icon=self.get_svg_icon("icons/delete.svg")
        )
        history_tool_button.set_enabled(False)
        history_tool_button.clicked.connect(self._show_files_history_dialog)

    def _show_files_history_dialog(self) -> None:
        self._history_dialog.show()


def main(parent: "QMainWindow", plugin_path: "Path"):
    return History(parent, plugin_path)
