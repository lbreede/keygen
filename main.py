import json
import logging.config
import pathlib

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

from model import Model

logger = logging.getLogger("main")


class View(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activate Software")

        self.username_field = QLineEdit()
        self.serial_field = QLineEdit()
        self.next_btn = QPushButton("Next >")
        self.cancel_btn = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addLayout(self.line_edit_layout("Username:", self.username_field))
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
    def username(self) -> str:
        return self.username_field.text().strip()

    @property
    def serial(self) -> str:
        """Serial without dashes"""
        return self.serial_field.text().replace("-", "")

    @property
    def serial_placeholder_text(self) -> str:
        ...

    @serial_placeholder_text.setter
    def serial_placeholder_text(self, text: str):
        self.serial_field.setPlaceholderText(text)

    @property
    def serial_max_length(self) -> int:
        ...

    @serial_max_length.setter
    def serial_max_length(self, length: int):
        self.serial_field.setMaxLength(length)


class Presenter:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.init_view()
        self.connect_signals()

    def init_view(self) -> None:
        logger.debug("Initializing view")
        self.view.serial_placeholder_text = "-".join(
            ["X" * (self.model.key_length // 5) for _ in range(5)]
        )
        self.view.serial_max_length = self.model.key_length + 4

    def connect_signals(self) -> None:
        logger.debug("Connecting signals")
        self.view.serial_field.textChanged.connect(self.format_serial)
        self.view.next_btn.clicked.connect(self.next_btn_clicked)
        self.view.cancel_btn.clicked.connect(self.view.close)

    def format_serial(self, text: str) -> None:
        text = "".join(c.upper() for c in text if c.isalnum())
        text = self.model.add_dashes(text)
        self.view.serial_field.setText(text)

    def next_btn_clicked(self):
        if self.model.check_key(self.view.username, self.view.serial):
            QMessageBox.information(
                self.view, "Success", "Your key is valid, you can proceed."
            )
            self.view.close()
        else:
            # TODO: Consider just logging, it gets annoying
            QMessageBox.warning(
                self.view, "Error", "Your key is invalid, please try again."
            )


def setup_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)


def main():
    setup_logging()

    app = QApplication([])

    model = Model()
    view = View()
    _ = Presenter(model, view)

    view.show()
    app.exec_()


if __name__ == "__main__":
    main()
