import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QLabel

from plugin.api import ContentTableAPI
from pieapp.structs.containers import Containers

from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class ContentTable(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    api = ContentTableAPI
    name = Containers.ContentTable

    def setColumns(self, count: int, columns: tuple = None) -> None:
        self.table.setColumnCount(count)
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(columns))

    def setTextAlignment(self, count: int) -> None:
        headers = self.table.horizontalHeader()
        for column in range(count):
            headers.horizontalHeaderItem(column).setTextAlignment(Qt.AlignCenter)

    def setColumnsStretch(self, count: int) -> None:
        headers = self.table.horizontalHeader()
        for column in range(count):
            headers.setSectionResizeMode(column, QHeaderView.Stretch)

    def fillTable(self, data: list[dict]) -> None:
        if not data:
            self.logger.error("No data were provided")
            return

        for row, item in enumerate(data):
            self.table.setItem(row, row, QTableWidgetItem(item))

        self.parent().mainLayout.addWidget(self.table, 1, 0)

    def setPlaceholder(self) -> None:
        placeholder = QLabel("<img src='{icon}' width=64 height=64><br>{text}".format(
            icon=self.getAsset("empty-box.png"),
            text=self.getTranslation("No files selected")
        ))
        placeholder.setAlignment(Qt.AlignCenter)
        self.parent().mainLayout.addWidget(placeholder, 1, 0)

    def init(self) -> None:
        self.table = QTableWidget()
        self.setPlaceholder()
        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )


def main(*args, **kwargs) -> typing.Any:
    return ContentTable(*args, **kwargs)