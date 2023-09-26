from __feature__ import snake_case

from PySide6.QtCore import QEvent
from PySide6.QtGui import Qt, QEnterEvent
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout, QSizePolicy

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent: "QObject" = None) -> None:
        super().__init__(parent)

        self._items: list[QToolButton] = []

        self._menu_hbox = QHBoxLayout()
        self._menu_hbox.set_contents_margins(1, 1, 1, 1)
        self._menu_hbox.insert_stretch(-1, 1)

        self.set_layout(self._menu_hbox)
        self.set_object_name("ConverterMenuWidget")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)
        self._menu_size_policy = self.size_policy()
        self._menu_size_policy.set_retain_size_when_hidden(True)
        self.set_size_policy(self._menu_size_policy)
        self.hide()

    @property
    def items(self) -> list[QToolButton]:
        return self._items

    @property
    def menu_size_policy(self) -> QSizePolicy:
        return self._menu_size_policy

    def add_item(self, name: str, item: QToolButton) -> None:
        if name in self._items:
            raise PieException(f"Item \"{item}\"")

        item.set_object_name("ConverterMenuItemTB")
        self._menu_hbox.add_widget(item, alignment=Qt.AlignmentFlag.AlignRight)

        self._items.append(item)
