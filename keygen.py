from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)
import logging
from model import Model
import pyperclip


class bcolors:
    DEBUG = "\033[94m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    CRITICAL = "\033[91m"
    ENDC = "\033[0m"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LEVEL_COLORS: tuple[tuple[int, str], ...] = (
    (logging.DEBUG, bcolors.DEBUG),
    (logging.INFO, bcolors.INFO),
    (logging.WARNING, bcolors.WARNING),
    (logging.ERROR, bcolors.ERROR),
    (logging.CRITICAL, bcolors.CRITICAL),
)

for level, color in LEVEL_COLORS:
    name = f"{color}{logging.getLevelName(level):^8}{bcolors.ENDC}"
    logging.addLevelName(level, name)


logger = logging.getLogger(__name__)


class View(QWidget):
    def __init__(self):
        super().__init__()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(100)
        self.username_field = QLineEdit("HazeBlaze420")
        self.username_field.setFixedWidth(300)

        serial_label = QLabel("Serial:")
        serial_label.setFixedWidth(100)
        self.serial_field = QLabel()
        self.serial_field.setFixedWidth(300)

        self.generate_btn = QPushButton("Generate")
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.cancel_btn = QPushButton("Cancel")

        username_field = self.line_edit_layout("Username:", self.username_field)
        serial_field = self.line_edit_layout("Serial:", self.serial_field)

        layout = QVBoxLayout()
        # layout.addLayout(grid_layout)
        layout.addLayout(username_field)
        layout.addLayout(serial_field)
        layout.addLayout(self.buttons_layout())
        self.setLayout(layout)

    def line_edit_layout(self, name: str, line_edit: QLineEdit | QLabel) -> QHBoxLayout:
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
    def username(self) -> str:
        return self.username_field.text()

    @property
    def serial(self) -> str:
        return self.serial_field.text()


class Presenter:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self) -> None:
        self.view.copy_btn.clicked.connect(self.copy_serial)
        self.view.generate_btn.clicked.connect(self.next_btn_clicked)
        self.view.cancel_btn.clicked.connect(self.view.close)

    def copy_serial(self) -> None:
        pyperclip.copy(self.view.serial)
        logger.info("Copied serial %r to clipboard", self.view.serial)

    def format_serial(self, text: str) -> None:
        text = "".join(c.upper() for c in text if c.isalnum())
        text = self.model.add_dashes(text)
        self.view.serial_field.setText(text)

    def next_btn_clicked(self):
        self.view.serial_field.setText(
            self.model.generate_key_with_dashes(self.view.username)
        )


if __name__ == "__main__":
    app = QApplication([])

    model = Model()
    view = View()
    presenter = Presenter(model, view)

    view.show()
    app.exec_()
