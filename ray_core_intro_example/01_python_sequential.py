import importlib.util
import time
from pathlib import Path
from types import ModuleType


def load_shared() -> ModuleType:
    """Load the shared helpers from `00_shared.py`.

    This is needed because filenames that start with numbers are not valid
    names for a normal Python import statement.
    """
    shared_path = Path(__file__).with_name("00_shared.py")
    spec = importlib.util.spec_from_file_location("shared", shared_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


shared = load_shared()

start = time.time()
data = [shared.retrieve(item) for item in range(8)]
shared.print_runtime(data, start)
