import logging

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model import KeyManager, Win95KeyManager

logger = logging.getLogger(__name__)


class View(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activate Software")

        self.serial_field = QLineEdit()
        self.next_btn = QPushButton("Next >")
        self.cancel_btn = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addLayout(self.line_edit_layout("Serial:", self.serial_field))
        layout.addLayout(self.buttons_layout())
        self.setLayout(layout)

    def line_edit_layout(self, name: str, line_edit: QLineEdit) -> QHBoxLayout:
        layout = QHBoxLayout()
        label = QLabel(name)
        label.setFixedWidth(100)
        line_edit.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout

    def buttons_layout(self) -> QHBoxLayout:
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.next_btn)
        buttons_layout.addWidget(self.cancel_btn)
        return buttons_layout

    @property
    def serial(self) -> str:
        return self.serial_field.text()

    @property
    def serial_max_length(self) -> int:
        ...

    @serial_max_length.setter
    def serial_max_length(self, length: int):
        self.serial_field.setMaxLength(length)


class Presenter:
    def __init__(self, model: KeyManager, view: View):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self) -> None:
        self.view.serial_field.textChanged.connect(self.format_serial)
        self.view.next_btn.clicked.connect(self.next_btn_clicked)
        self.view.cancel_btn.clicked.connect(self.view.close)

    def format_serial(self, text: str) -> None:
        self.view.serial_field.setText(self.model.format_key(text))

    def next_btn_clicked(self):
        if self.model.validate_key(self.view.serial):
            QMessageBox.information(
                self.view, "Success", "Your key is valid, you can proceed."
            )
            self.view.close()
        else:
            QMessageBox.warning(
                self.view, "Error", "Your key is invalid, please try again."
            )


def main() -> None:
    app = QApplication([])

    model = Win95KeyManager()
    view = View()
    _ = Presenter(model, view)

    view.show()
    app.exec_()


if __name__ == "__main__":
    main()
