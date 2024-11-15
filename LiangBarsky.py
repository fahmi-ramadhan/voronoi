from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, NamedTuple
from LineSegment import LineSegment
from Site import Site

class LiangBarskyResult(NamedTuple):
    is_origin_clipped: bool
    is_destination_clipped: bool
    result_segment: Optional[LineSegment]

class ClipperEdge(Enum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()

@dataclass
class Clipper:
    left: float
    right: float
    top: float
    bottom: float

def lb_clip(line: LineSegment, clipper: Clipper) -> LiangBarskyResult:
    """
    Liang-Barsky line clipping algorithm implementation
    Based on:
    - Liang-Barsky function by Daniel White
      http://www.skytopia.com/project/articles/compsci/clipping.html
    - Paper
      https://www.cs.helsinki.fi/group/goa/viewing/leikkaus/intro.html
    
    Args:
        line: The line segment to clip
        clipper: The clipping rectangle
    
    Returns:
        A tuple containing:
        - Whether the origin point was clipped
        - Whether the destination point was clipped
        - The resulting clipped line segment (or None if completely outside)
    """
    t0 = 0.0
    t1 = 1.0
    dx = line.b.x - line.a.x
    dy = line.b.y - line.a.y
    
    is_origin_clipped = False
    is_destination_clipped = False
    
    for edge in ClipperEdge:
        if edge == ClipperEdge.LEFT:
            p = -dx
            q = -(clipper.left - line.a.x)
        elif edge == ClipperEdge.RIGHT:
            p = dx
            q = (clipper.right - line.a.x)
        elif edge == ClipperEdge.TOP:
            p = -dy
            q = -(clipper.top - line.a.y)
        else:  # BOTTOM
            p = dy
            q = (clipper.bottom - line.a.y)
        
        if p == 0 and q < 0:
            # Don't draw line at all (parallel line outside)
            return LiangBarskyResult(False, False, None)
        
        if p != 0:
            r = q / p
            
            if p < 0:
                if r > t1:
                    # Don't draw line at all
                    return LiangBarskyResult(False, False, None)
                elif r > t0:
                    # Line is clipped!
                    is_origin_clipped = True
                    t0 = r
            elif p > 0:
                if r < t0:
                    # Don't draw line at all
                    return LiangBarskyResult(False, False, None)
                elif r < t1:
                    # Line is clipped!
                    is_destination_clipped = True
                    t1 = r
    
    # Calculate clipped line segment
    clipped_segment = LineSegment(
        a=Site(
            x=line.a.x + t0 * dx,
            y=line.a.y + t0 * dy
        ),
        b=Site(
            x=line.a.x + t1 * dx,
            y=line.a.y + t1 * dy
        )
    )
    
    return LiangBarskyResult(is_origin_clipped, is_destination_clipped, clipped_segment)