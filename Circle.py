from dataclasses import dataclass
from math import hypot
from typing import Optional
from Site import Site

Point = Site

@dataclass
class Circle:
    """
    Kelas yang merepresentasikan lingkaran dengan titik pusat dan jari-jari.
    """
    center: Point
    radius: float
    
    @classmethod
    def from_three_points(cls, p1: Point, p2: Point, p3: Point) -> Optional['Circle']:
        """
        Membuat lingkaran dari tiga titik yang diberikan.
        Referensi: https://www.xarg.org/2018/02/create-a-circle-out-of-three-points/
        
        Args:
            p1: Titik pertama
            p2: Titik kedua
            p3: Titik ketiga
            
        Returns:
            Objek Circle jika ketiga titik membentuk lingkaran yang valid,
            None jika tidak membentuk lingkaran yang valid
        """
        # Ambil koordinat x dan y dari ketiga titik
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        
        # Hitung determinan untuk mencari pusat lingkaran
        a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
        
        # Hitung komponen x dari pusat lingkaran
        b = ((x1 * x1 + y1 * y1) * (y3 - y2) + 
             (x2 * x2 + y2 * y2) * (y1 - y3) + 
             (x3 * x3 + y3 * y3) * (y2 - y1))
        
        # Hitung komponen y dari pusat lingkaran
        c = ((x1 * x1 + y1 * y1) * (x2 - x3) + 
             (x2 * x2 + y2 * y2) * (x3 - x1) + 
             (x3 * x3 + y3 * y3) * (x1 - x2))
        
        # Cek apakah ketiga titik segaris (kolinear)
        if a == 0:
            return None
            
        # Hitung koordinat pusat lingkaran
        x = -b / (2 * a)
        y = -c / (2 * a)
        
        # Buat objek Point untuk pusat lingkaran
        center = Point(x=x, y=y)
        # Hitung jari-jari menggunakan jarak dari pusat ke salah satu titik
        radius = hypot(x - x1, y - y1)
        
        return cls(center=center, radius=radius)
    
    @property
    def bottom_point(self) -> Point:
        """
        Mengembalikan titik dengan koordinat Y maksimum pada lingkaran
        (titik terbawah pada lingkaran).
        
        Returns:
            Point: Titik dengan koordinat y = y_pusat + jari_jari
        """
        return Point(
            x=self.center.x,
            y=self.center.y + self.radius
        )
