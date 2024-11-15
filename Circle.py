from dataclasses import dataclass
from math import hypot
from typing import Optional
from Site import Site

# Type aliases
Point = Site

@dataclass
class Circle:
    center: Point
    radius: float
    
    @classmethod
    def from_three_points(cls, p1: Point, p2: Point, p3: Point) -> Optional['Circle']:
        """
        Defines circle by three points
        See: https://www.xarg.org/2018/02/create-a-circle-out-of-three-points/
        
        Args:
            p1: First point
            p2: Second point
            p3: Third point
            
        Returns:
            Circle instance if three points define a circle, None otherwise
        """
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        
        a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
        
        b = ((x1 * x1 + y1 * y1) * (y3 - y2) + 
             (x2 * x2 + y2 * y2) * (y1 - y3) + 
             (x3 * x3 + y3 * y3) * (y2 - y1))
        
        c = ((x1 * x1 + y1 * y1) * (x2 - x3) + 
             (x2 * x2 + y2 * y2) * (x3 - x1) + 
             (x3 * x3 + y3 * y3) * (x1 - x2))
        
        if a == 0:
            return None
            
        x = -b / (2 * a)
        y = -c / (2 * a)
        
        center = Point(x=x, y=y)
        radius = hypot(x - x1, y - y1)
        
        return cls(center=center, radius=radius)
    
    @property
    def bottom_point(self) -> Point:
        """Returns a point with maximum Y coordinate"""
        return Point(
            x=self.center.x,
            y=self.center.y + self.radius
        )