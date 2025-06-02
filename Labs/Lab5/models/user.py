from dataclasses import dataclass, field
from typing import Optional
from functools import total_ordering

@dataclass
@total_ordering
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: Optional[str] = None
    address: Optional[str] = None

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
