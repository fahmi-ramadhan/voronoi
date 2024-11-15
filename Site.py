from typing import Any, Optional
from dataclasses import dataclass
from Vector import Vector2D

@dataclass
class Site:
    x: float
    y: float
    satellite: Optional[Any] = None
    
    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: 'Site') -> bool:
        if not isinstance(other, Site):
            return NotImplemented
        return (self.x == other.x and 
                self.y == other.y)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    @property
    def vector(self) -> Vector2D:
        return Vector2D(dx=self.x, dy=self.y)
    
    def distance_to(self, point: 'Site') -> float:
        """Calculate the distance to another point."""
        x_dist = self.x - point.x
        y_dist = self.y - point.y
        return (x_dist * x_dist + y_dist * y_dist) ** 0.5