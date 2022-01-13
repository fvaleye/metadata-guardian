import os

from rich.logging import RichHandler


def configure_logger() -> None:
    """
    Configure the loguru configuration with Rich.

    :return:
    """
    if "LOGURU_LEVEL" not in os.environ:
        os.environ["LOGURU_LEVEL"] = "INFO"
    from loguru import logger

    logger.configure(
        handlers=[{"sink": RichHandler(markup=True), "format": "{message}"}]
    )


configure_logger()
