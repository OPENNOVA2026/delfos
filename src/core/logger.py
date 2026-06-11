import logging

from rich.console import Console
from rich.logging import RichHandler

from core.settings import settings

console = Console()

rich_handler = RichHandler(
    console=console,
    show_time=False,
    show_level=False,
    markup=True,
    rich_tracebacks=True,
)
rich_handler.setFormatter(
    logging.Formatter(
        r"[%(levelname)s] \[%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)

logger = logging.getLogger("delfos")
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
logger.addHandler(rich_handler)

logger.propagate = False
