import typing

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QGridLayout, QPushButton, QDialog

from pieapp.structs.menus import Menus
from piekit.managers.structs import Sections
from piekit.plugins.plugins import PiePlugin
from pieapp.structs.plugins import Plugins
from pieapp.structs.containers import Containers
from piekit.managers.menus.mixins import MenuAccessor

from piekit.config import Config
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import onPluginAvailable


class About(
    PiePlugin,
    MenuAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Plugins.About
    requires = [Containers.MenuBar]

    def init(self) -> None:
        self.dialog = QDialog(self.parent())
        self.dialog.setWindowTitle(self.getTranslation("About"))
        self.dialog.setWindowIcon(self.getPluginIcon())
        self.dialog.resize(400, 300)

        okButton = QPushButton(self.getTranslation("Ok"))
        okButton.clicked.connect(self.dialog.close)

        pixmap = QPixmap()
        pixmap.load(self.getAsset("cloud.png"))

        iconLabel = QLabel()
        iconLabel.setPixmap(pixmap)

        descriptionLabel = QLabel()
        descriptionLabel.setText("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))

        githubLinkLabel = QLabel()
        githubLinkLabel.setOpenExternalLinks(True)
        githubLinkLabel.setText("<a href='https://github.com/uselessvevo/pie-audio/'>Project URL</a>")

        gridLayout = QGridLayout()
        gridLayout.addWidget(iconLabel, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        gridLayout.addWidget(descriptionLabel, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        gridLayout.addWidget(githubLinkLabel, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        gridLayout.addWidget(okButton, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.dialog.setLayout(gridLayout)

    @onPluginAvailable(target=Containers.MenuBar)
    def onMenuBarAvailable(self) -> None:
        self.addMenuItem(
            section=Sections.Shared,
            menu=Menus.Help,
            name="about",
            text=self.getTranslation("About"),
            triggered=self.dialog.show,
            icon=self.getAssetIcon("help.png"),
        )


def main(*args, **kwargs) -> typing.Any:
    return About(*args, **kwargs)