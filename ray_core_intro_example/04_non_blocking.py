import importlib.util
import os
import time
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

os.environ["RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO"] = "0"

import ray


def load_shared() -> ModuleType:
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
    return shared.retrieve(item, db)


start = time.time()
db_object_ref = ray.put(shared.database)

pending_refs = [
    retrieve_task.remote(item, db_object_ref) for item in range(8)
]

all_data: list[tuple[int, str]] = []

while pending_refs:
    ready_refs, pending_refs = ray.wait(
        pending_refs,
        num_returns=1,
        timeout=1.0,
    )

    if not ready_refs:
        print(f"{time.time() - start:.2f}s: nothing finished yet")
        continue

    new_data = ray.get(ready_refs)
    print(f"{time.time() - start:.2f}s: just finished -> {new_data}")
    all_data.extend(new_data)

print("\nFinal results in completion order:")
print(*all_data, sep="\n")

print("\nFinal results sorted by item:")
print(*sorted(all_data), sep="\n")