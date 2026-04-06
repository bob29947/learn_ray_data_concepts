import os
import time
from collections.abc import Sequence

database = [
    "Learning",
    "Ray",
    "Flexible",
    "Distributed",
    "Python",
    "for",
    "Machine",
    "Learning",
]


def retrieve(item: int, db: Sequence[str] | None = None) -> tuple[int, str]:
    """Return the word at index `item` from the fake database.

    Args:
        item: The position to look up in the database list.
        db: An optional database list to use instead of the shared default.
    """
    if db is None:
        db = database
    time.sleep(item / 10.0)
    return item, db[item]


def describe_database(label: str, db: Sequence[str]) -> str:
    """Return a short description of a database reference.
    
    Gives us process id, database id, database length, is it original module global

    Args:
        label: A human-readable label describing the reference.
        db: The database object being described.

    Returns:
        A formatted string with process and object identity details.
    """
    return (
        f"{label}: pid={os.getpid()}, python_id={id(db)}, "
        f"len={len(db)}, is_module_database={db is database}"
    )


def print_database_references(title: str, references: Sequence[str]) -> None:
    """Print a labeled list of database reference descriptions.

    Args:
        title: The section title to print before the references.
        references: The formatted database reference descriptions.
    """
    print(title)
    print(*references, sep="\n")
    print()


def print_runtime(input_data: Sequence[tuple[int, str]], start_time: float) -> None:
    """Print the elapsed runtime and each returned record.

    Args:
        input_data: The results collected from the database lookups.
        start_time: The timestamp captured before the work started.
    """
    print(f"Runtime: {time.time() - start_time:.2f} seconds, data:")
    print(*input_data, sep="\n")
