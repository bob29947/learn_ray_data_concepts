import importlib.util
import os
import time
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

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
def retrieve_task(item: int, db: Sequence[str]) -> tuple[int, str]:
    """Run one database lookup as a Ray task.

    Args:
        item: The position to look up in the shared fake database.
        db: The fake database loaded from Ray's object store.
    """
    return shared.retrieve(item, db)


@ray.remote
def inspect_database_task(db: Sequence[str]) -> str:
    """Describe the database visible inside one Ray worker process.

    Args:
        db: The fake database loaded from Ray's object store.

    Returns:
        A formatted description of the worker's database reference.
    """
    return shared.describe_database("03 worker object-store db", db)


db_object_ref = ray.put(shared.database)
driver_object_store_database = ray.get(db_object_ref)

database_references = [
    shared.describe_database("03 driver shared.database", shared.database),
    shared.describe_database(
        "03 driver ray.get(db_object_ref)", driver_object_store_database
    ),
    f"03 driver db_object_ref={db_object_ref}",
    (
        "03 driver shared.database is ray.get(db_object_ref): "
        f"{shared.database is driver_object_store_database}"
    ),
]
database_references.extend(
    ray.get([inspect_database_task.remote(db_object_ref) for _ in range(4)])
)
shared.print_database_references("03 database references:", database_references)

start = time.time()

object_references = [
    retrieve_task.remote(item, db_object_ref) for item in range(8)
]

data = ray.get(object_references)
shared.print_runtime(data, start)
