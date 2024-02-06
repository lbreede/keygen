import json
import logging.config
import pathlib

from PyQt5.QtWidgets import QApplication

from key_manager import Win95KeyManager
from keygen import KeygenCtrl, KeygenUI
from software import Presenter as SoftwarePresenter
from software import ViewBuilder, ViewPreset

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

    model = Win95KeyManager()
    SoftwarePresenter(model, win95_view := ViewBuilder.build(ViewPreset.WIN95))
    KeygenCtrl(model, keygen_view := KeygenUI())

    win95_view.move(100, 100)
    keygen_view.move(300, 300)

    win95_view.show()
    keygen_view.show()

    app.exec_()


if __name__ == "__main__":
    main()
