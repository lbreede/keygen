import logging

import pyperclip  # type: ignore
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from key_manager import KeyManager, Win95KeyManager

logger = logging.getLogger(__name__)


class KeygenUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keygen")

        serial_label = QLabel("Serial:")
        serial_label.setFixedWidth(100)
        self.serial_field = QLabel()
        self.serial_field.setFixedWidth(300)

        self.generate_btn = QPushButton("Generate")
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.cancel_btn = QPushButton("Cancel")

        serial_field = self.line_edit_layout("Serial:", self.serial_field)

        layout = QVBoxLayout()
        layout.addLayout(serial_field)
        layout.addLayout(self.buttons_layout())
        self.setLayout(layout)

    def line_edit_layout(
        self, name: str, line_edit: QLineEdit | QLabel
    ) -> QHBoxLayout:
        layout = QHBoxLayout()
        label = QLabel(name)
        label.setFixedWidth(100)
        line_edit.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout

    def buttons_layout(self) -> QHBoxLayout:
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.copy_btn)
        buttons_layout.addWidget(self.cancel_btn)
        return buttons_layout

    @property
    def serial(self) -> str:
        return self.serial_field.text()


class KeygenCtrl:
    def __init__(self, key_manager: KeyManager, view: KeygenUI):
        self.key_manager = key_manager
        self.view = view
        self.connect_signals()

    def connect_signals(self) -> None:
        self.view.copy_btn.clicked.connect(self.copy_serial)
        self.view.generate_btn.clicked.connect(self.next_btn_clicked)
        self.view.cancel_btn.clicked.connect(self.view.close)

    def copy_serial(self) -> None:
        pyperclip.copy(self.view.serial)  # type: ignore
        logger.info("Copied serial %r to clipboard", self.view.serial)

    def next_btn_clicked(self):
        self.view.serial_field.setText(self.key_manager.generate_key())


def main():
    app = QApplication([])

    model = Win95KeyManager()
    view = KeygenUI()
    _ = KeygenCtrl(model, view)

    view.show()
    app.exec_()


if __name__ == "__main__":
    main()
