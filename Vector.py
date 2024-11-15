from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Site import Site

@dataclass
class Vector2D:
    dx: float = 0.0
    dy: float = 0.0
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector addition"""
        return Vector2D(dx=self.dx + other.dx, dy=self.dy + other.dy)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector subtraction"""
        return Vector2D(dx=other.dx - self.dx, dy=other.dy - self.dy)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        """Vector multiplication with scalar (vector * scalar)"""
        return Vector2D(dx=self.dx * scalar, dy=self.dy * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector2D':
        """Vector multiplication with scalar (scalar * vector)"""
        return Vector2D(dx=self.dx * scalar, dy=self.dy * scalar)
    
    @property
    def magnitude(self) -> float:
        """Vector magnitude (length)"""
        return sqrt(self.dx * self.dx + self.dy * self.dy)
    
    @property
    def normal(self) -> 'Vector2D':
        """Normal vector"""
        return Vector2D(dx=-self.dy, dy=self.dx)
    
    @property
    def point(self) -> 'Site':
        """Convert to Site"""
        from Site import Site
        return Site(x=self.dx, y=self.dy)