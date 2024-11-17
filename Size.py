from dataclasses import dataclass

@dataclass
class Size:
    """
    Merepresentasikan ukuran dari objek berbentuk persegi panjang.
    
    Attributes:
        width (float): Lebar dari persegi panjang
        height (float): Tinggi dari persegi panjang
    """
    width: float
    height: float
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
