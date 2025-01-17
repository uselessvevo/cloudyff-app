from __feature__ import snake_case

from PySide6.QtCore import QEvent, QRect, Signal
from PySide6.QtGui import QAction
from PySide6.QtGui import QCursor
from PySide6.QtGui import QEnterEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QToolTip

from pieapp.api.globals import Global
from pieapp.api.registries.locales.helpers import translate


class ImagePreview(QToolTip):

    def __init__(self, parent, image_path: str) -> None:
        self._parent = parent
        self._string = "<img width=264 height=264 src='%s'>" % image_path if image_path else None
        super(ImagePreview, self).__init__()

    def show_tooltip(self) -> None:
        if self._string:
            self.show_text(QCursor.pos(), self._string, self._parent, QRect(), 10000)


class AlbumCoverPicker(QLineEdit):
    sig_album_cover_changed = Signal(str, str)

    def __init__(
        self,
        parent: "QObject" = None,
        media_file_name: str = None,
        image_path: str = None,
        picker_icon: QIcon = None,
        placeholder_text: str = "No image selected",
        select_album_cover_text: str = "Select album cover image"
    ) -> None:
        super(AlbumCoverPicker, self).__init__(parent)

        self._media_file_name = media_file_name
        self._image_path = image_path
        self._placeholder_text = f"<{placeholder_text}>"
        self._select_album_cover_text = select_album_cover_text
        self._image_preview = ImagePreview(self, self._image_path)

        self._add_image_button = QLineEdit()
        self._add_image_action = QAction()
        self._add_image_action.set_icon(picker_icon or self.style().standard_icon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self._add_image_action.triggered.connect(self.load_image)

        self.set_read_only(True)
        self.insert(self._image_path if self._image_path else self._placeholder_text)
        self.add_action(self._add_image_action, QLineEdit.ActionPosition.TrailingPosition)

    def enter_event(self, event: QEnterEvent) -> None:
        """
        Show tooltip with a picture miniature
        """
        self._image_preview.show_tooltip()

    def leave_event(self, event: QEvent) -> None:
        """
        Hide tooltip with a picture miniature
        """
        self._image_preview.hide_text()

    def set_picker_icon(self, icon: QIcon) -> None:
        self._add_image_action.set_icon(icon)

    def set_prepare_image_method(self, method: callable) -> None:
        setattr(self, method.__qualname__, method)

    def set_load_image_method(self, method: callable) -> None:
        setattr(self, method.__qualname__, method)

    def prepare_image(self) -> None:
        pass

    def load_image(self, image_path=None) -> None:
        image_path = image_path if image_path else self._image_path
        file_path = QFileDialog.get_open_file_name(
            parent=self,
            caption=translate(self._select_album_cover_text),
            dir=image_path or str(Global.USER_ROOT),
        )
        if file_path[0]:
            self.clear()
            image_path = file_path[0]
            self.insert(image_path)
            self._image_preview = ImagePreview(self, file_path[0])

        self._image_path = image_path
        self.sig_album_cover_changed.emit(self._media_file_name, image_path)
