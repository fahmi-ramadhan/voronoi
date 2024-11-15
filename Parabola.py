import math
from dataclasses import dataclass
from Site import Site

class Parabola:
    def __init__(self, focus: Site, directrix_y: float):
        """
        Constructor that defines parabola by the focus and the directrix that is parallel to X-axis
        
        Args:
            focus: Parabola focus point
            directrix_y: Directrix Y coordinate
        """
        self.focus = focus
        self.directrix_y = directrix_y
    
    @property
    def standard_form(self) -> tuple[float, float, float]:
        """
        Converts parabola to standard form (ax^2 + bx + c)
        
        Returns:
            Tuple of coefficients (a, b, c)
        """
        # X coord of parabola vertex
        vx = (self.focus.y + self.directrix_y) / 2
        # Y coord of parabola vertex
        vy = (self.focus.y - self.directrix_y) / 2
        
        a = 1 / (4 * vy)
        b = (-1 * self.focus.x) / (2 * vy)
        c = (self.focus.x * self.focus.x) / (4 * vy) + vx
        
        return (a, b, c)
    
    def resolve(self, x: float) -> float:
        """
        Resolves parabola equation against given X
        
        Args:
            x: X coordinate to evaluate
            
        Returns:
            Y coordinate at given X
        """
        a, b, c = self.standard_form
        y = a * (x * x) + b * x + c
        return y
    
    def to_quad_bezier(self, min_x: float, max_x: float) -> tuple[Site, Site, Site]:
        """
        Quadratic Bezier representation of the Parabola clipped by X
        
        Args:
            min_x: Min X clipping point
            max_x: Max X clipping point
            
        Returns:
            Tuple of (start point, control point, end point)
        """
        min_x, max_x = min(min_x, max_x), max(min_x, max_x)
        
        a, b, _ = self.standard_form
        start = Site(x=min_x, y=self.resolve(min_x))
        end = Site(x=max_x, y=self.resolve(max_x))
        
        cx = (min_x + max_x) / 2
        cy = (max_x - min_x) / 2 * (2 * a * min_x + b) + self.resolve(min_x)
        cp = Site(x=cx, y=cy)
        
        return (start, cp, end)
    
    def intersection_x(self, parabola: 'Parabola') -> float | None:
        """
        X coordinate of the intersection with other Parabola (if present)
        
        Args:
            parabola: Other parabola to find intersection with
            
        Returns:
            X coordinate of intersection or None if no intersection exists
        """
        focus_left = self.focus
        focus_right = parabola.focus
        directrix = self.directrix_y
        
        # Handle the degenerate case when two parabolas have the same Y
        # If two parabolas have the same Y, then the intersection lies exactly at the middle between them
        if focus_left.y == focus_right.y:
            return (focus_left.x + focus_right.x) / 2
        
        # Handle the degenerate case where one or both of the sites have the same Y value
        # In this case the focus of one or both sites and the directrix would be equal
        if focus_left.y == directrix:
            return focus_left.x
        elif focus_right.y == directrix:
            return focus_right.x
            
        # Determine the a, b and c coefficients for the two parabolas
        a1, b1, c1 = self.standard_form
        a2, b2, c2 = parabola.standard_form
        
        # Calculate the roots of the coefficients difference
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2
        
        discriminant = b * b - 4 * a * c
        
        try:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            
            # X of the intersection is one of those roots
            x = min(x1, x2) if focus_left.y < focus_right.y else max(x1, x2)
            
            return None if math.isnan(x) else x
            
        except (ValueError, ZeroDivisionError):
            return None