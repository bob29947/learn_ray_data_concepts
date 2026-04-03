import importlib.util
import time
from pathlib import Path
from types import ModuleType

import ray


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

ray.init()


@ray.remote
def retrieve_task(item: int) -> tuple[int, str]:
    """Run one database lookup as a Ray task.

    Args:
        item: The position to look up in the shared fake database.
    """
    return shared.retrieve(item)


start = time.time()

object_references = [retrieve_task.remote(item) for item in range(8)]

data = ray.get(object_references)
shared.print_runtime(data, start)
