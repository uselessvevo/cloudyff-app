from __feature__ import snake_case

from dataclasses import dataclass as dt

from PySide6.QtWidgets import QPushButton


@dt(frozen=True, eq=False, slots=True)
class ButtonRole:
    Default = "QPushButton"
    Flat = "FlatButton"
    Primary = "PrimaryButton"
    Danger = "DangerButton"
    DangerFlat = "DangerFlatButton"


class Button(QPushButton):

    def __init__(self, role: str = ButtonRole.Default, *args, **kwargs) -> None:
        super(Button, self).__init__(*args, **kwargs)
        self.set_object_name(role)
