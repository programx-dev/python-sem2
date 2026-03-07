import pkgutil
import importlib
from pathlib import Path


def discover_sources():
    """
    Автоматически импортирует все модули в текущей папке для срабатывания декораторов.
    """
    package_path = str(Path(__file__).parent)
    for _, name, is_pkg in pkgutil.iter_modules([package_path]):
        if not is_pkg and name != "repository":
            importlib.import_module(f"src.sources.{name}")


discover_sources()
