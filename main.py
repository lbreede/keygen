import json
import logging.config
import pathlib

from PyQt5.QtWidgets import QApplication

from key_manager import Win95KeyManager
from keygen import KeygenUI
from keygen import Presenter as KeygenPresenter
from software import Presenter as SoftwarePresenter
from software import View as SoftwareView

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as fp:
        config = json.load(fp)
    logging.config.dictConfig(config)


def main() -> None:
    setup_logging()
    logger.info("Starting application")

    app = QApplication([])

    model = Win95KeyManager()  # Be mindful this is shared between the two views

    software_view = SoftwareView()
    _software_presenter = SoftwarePresenter(model, software_view)
    software_view.move(100, 100)

    keygen_view = KeygenUI()
    _keygen_presenter = KeygenPresenter(model, keygen_view)
    keygen_view.move(300, 300)

    software_view.show()
    keygen_view.show()

    app.exec_()


if __name__ == "__main__":
    main()
