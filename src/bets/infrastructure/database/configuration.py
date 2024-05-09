import os
from dataclasses import dataclass
from typing import Self


@dataclass
class DatabaseConfiguration:
    dsn: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            dsn=os.environ['DB_DSN'],
        )
