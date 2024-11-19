from dataclasses import dataclass
from Constant import eps
from Site import Site

@dataclass
class LineSegment:
    """
    Merepresentasikan sebuah segmen garis antara dua titik dalam ruang 2D.
    
    Attributes:
        a: Titik ujung pertama dari segmen garis
        b: Titik ujung kedua dari segmen garis
    """
    a: Site
    b: Site
    
    def contains_point(self, point: Site) -> bool:
        """
        Memeriksa apakah suatu titik terletak pada segmen garis.
        
        Method ini menggunakan pendekatan berikut:
        1. Untuk garis vertikal, periksa apakah x koordinat titik sama dengan x garis
           dan y koordinat berada di antara kedua ujung garis
        2. Untuk garis lainnya, hitung gradien (k) dan intersep-y (c),
           kemudian periksa apakah titik memenuhi persamaan garis y = kx + c
        
        Args:
            point: Titik yang akan diperiksa
            
        Returns:
            True jika titik terletak pada segmen garis, False jika tidak
        
        Note:
            Menggunakan nilai epsilon (eps) untuk perbandingan floating-point
            untuk mengatasi masalah presisi numerik
        """
        # Kasus khusus untuk garis vertikal
        if abs(self.b.x - self.a.x) < eps:
            return (
                abs(point.x - self.a.x) < eps  # x koordinat sama
                and point.y >= min(self.a.y, self.b.y)  # y di antara kedua ujung
                and point.y <= max(self.a.y, self.b.y)
            )
        
        # Hitung gradien dan intersep-y
        k = (self.b.y - self.a.y) / (self.b.x - self.a.x)
        c = self.a.y - k * self.a.x
        
        # Periksa apakah titik terletak pada garis
        return abs(point.y - (point.x * k + c)) < eps
