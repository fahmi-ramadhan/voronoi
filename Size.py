from dataclasses import dataclass

@dataclass
class Size:
    """Represents the size of a Rectangular object.
    
    Attributes:
        width (float): The width of the rectangle
        height (float): The height of the rectangle
    """
    width: float
    height: float
    
    def __init__(self, width: float, height: float):
        """Initialize a new Size instance.
        
        Args:
            width (float): The width of the rectangle
            height (float): The height of the rectangle
        """
        self.width = width
        self.height = height