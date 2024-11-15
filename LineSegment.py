from dataclasses import dataclass
from math import sqrt

# Small value for floating-point comparisons
eps = 1e-10

@dataclass
class Site:
    """Represents a point in 2D space."""
    x: float
    y: float

@dataclass
class LineSegment:
    """Represents a line segment between two points in 2D space.
    
    Attributes:
        a (Site): First endpoint of the line segment
        b (Site): Second endpoint of the line segment
    """
    a: Site
    b: Site
    
    def contains_point(self, point: Site) -> bool:
        """Check if a point lies on the line segment.
        
        Args:
            point (Site): The point to check
            
        Returns:
            bool: True if the point lies on the line segment, False otherwise
        """
        # Special case for vertical lines
        if abs(self.b.x - self.a.x) < eps:
            return (
                abs(point.x - self.a.x) < eps
                and point.y >= min(self.a.y, self.b.y)
                and point.y <= max(self.a.y, self.b.y)
            )
        
        # Calculate slope and y-intercept
        k = (self.b.y - self.a.y) / (self.b.x - self.a.x)
        c = self.a.y - k * self.a.x
        
        # Check if point lies on the line
        return abs(point.y - (point.x * k + c)) < eps
    
    def length(self) -> float:
        """Calculate the length of the line segment.
        
        Returns:
            float: The length of the line segment
        """
        x_dist = self.a.x - self.b.x
        y_dist = self.a.y - self.b.y
        return sqrt(x_dist * x_dist + y_dist * y_dist)