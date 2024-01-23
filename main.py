import json
import logging
import logging.config
import pathlib

from PyQt5.QtWidgets import QApplication

from keygen import Presenter as KeygenPresenter
from keygen import View as KeygenView
from model import Model
from software import Presenter as SoftwarePresenter
from software import View as SoftwareView

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)


def main() -> None:
    setup_logging()
    logger.info("Starting application")

    app = QApplication([])
    # model = Model()

    software_view = SoftwareView()
    software_presenter = SoftwarePresenter(Model(), software_view)

    keygen_view = KeygenView()
    keygen_presenter = KeygenPresenter(Model(), keygen_view)

    software_view.show()
    keygen_view.show()

    app.exec_()


if __name__ == "__main__":
    main()
