"""Save and load records as CSV files in the data/ folder.

Each "name" is one table. load("bookings") reads data/bookings.csv and gives
you a list of dictionaries. Open the file in the editor any time to see
exactly what your app has stored — there is no hidden database.
"""

import csv
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _path_for(name: str, data_dir: Path | None) -> Path:
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{name}.csv"


def load(name: str, data_dir: Path | None = None) -> list[dict[str, str]]:
    """Read every record. Returns [] if nothing has been saved yet."""
    path = _path_for(name, data_dir)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(name: str, records: list[dict[str, str]], data_dir: Path | None = None) -> None:
    """Overwrite everything with the given records."""
    path = _path_for(name, data_dir)
    if not records:
        path.write_text("", encoding="utf-8")
        return
    columns = list(records[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)


def append(name: str, record: dict[str, str], data_dir: Path | None = None) -> None:
    """Add one record to the end, keeping existing records."""
    existing = load(name, data_dir)
    if existing and set(record.keys()) != set(existing[0].keys()):
        raise ValueError(
            f"columns do not match: {name}.csv has {sorted(existing[0])}, "
            f"you gave {sorted(record)}"
        )
    save(name, existing + [record], data_dir)
