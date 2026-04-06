import importlib.util
import os
import time
from pathlib import Path
from types import ModuleType

# Keep Ray from printing a future-facing GPU environment warning in this CPU-only example.
os.environ["RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO"] = "0"

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
def inspect_database_task() -> str:
    """Describe the database visible inside one Ray worker process.

    Returns:
        A formatted description of the worker's database reference.
    """
    return shared.describe_database("02 worker shared.database", shared.database)


@ray.remote
def retrieve_task(item: int) -> tuple[int, str]:
    """Run one database lookup as a Ray task.

    Args:
        item: The position to look up in the shared fake database.
    """
    return shared.retrieve(item)


database_references = [shared.describe_database("02 driver shared.database", shared.database)]
database_references.extend(ray.get([inspect_database_task.remote() for _ in range(4)]))
shared.print_database_references("02 database references:", database_references)

start = time.time()

object_references = [retrieve_task.remote(item) for item in range(8)]

data = ray.get(object_references)
shared.print_runtime(data, start)
