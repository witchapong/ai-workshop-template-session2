"""Example data shape. Copy this pattern for your own project's data.

A dataclass describes ONE thing your app stores — a booking, a part, a reading.
`to_dict` and `from_dict` convert it to and from the plain dictionaries that
core/storage.py writes to CSV files.
"""

import uuid
from dataclasses import dataclass, asdict


def new_id() -> str:
    """Return a short unique identifier, e.g. '3f2a9c01'."""
    return uuid.uuid4().hex[:8]


@dataclass
class Item:
    """One row of example data. Replace this with your own."""

    id: str
    name: str
    note: str

    def to_dict(self) -> dict[str, str]:
        """Convert to a plain dictionary of strings, ready for storage."""
        return {key: str(value) for key, value in asdict(self).items()}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Item":
        """Rebuild an Item from a dictionary read back out of storage."""
        return cls(id=data["id"], name=data["name"], note=data["note"])
