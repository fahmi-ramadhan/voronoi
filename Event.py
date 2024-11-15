from enum import Enum
from dataclasses import dataclass
from typing import Optional
from Beachline import Arc
import Site
from Circle import Circle

class EventKind(Enum):
    SITE = "site"
    CIRCLE = "circle"

@dataclass
class Event:
    point: 'Site'
    kind: EventKind = EventKind.SITE
    # Circle event only
    arc: Optional['Arc'] = None
    circle: Optional['Circle'] = None

    def __eq__(self, other: 'Event') -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.point == other.point and self.kind == other.kind

    def __lt__(self, other: 'Event') -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        if self.point.y == other.point.y:
            return self.point.x < other.point.x
        return self.point.y < other.point.y