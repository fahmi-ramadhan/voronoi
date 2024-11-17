from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Site import Site

@dataclass
class Vector2D:
    """
    Merepresentasikan vektor dua dimensi dengan komponen x dan y.
    
    Attributes:
        dx (float): Komponen x dari vektor (default: 0.0)
        dy (float): Komponen y dari vektor (default: 0.0)
    """
    dx: float = 0.0
    dy: float = 0.0
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """
        Melakukan penjumlahan vektor.
        
        Args:
            other: Vektor yang akan dijumlahkan
            
        Returns:
            Vector2D: Hasil penjumlahan kedua vektor
            
        Note:
            v3 = v1 + v2 menghasilkan vektor dengan komponen:
            dx = v1.dx + v2.dx
            dy = v1.dy + v2.dy
        """
        return Vector2D(dx=self.dx + other.dx, dy=self.dy + other.dy)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """
        Melakukan pengurangan vektor.
        
        Args:
            other: Vektor pengurang
            
        Returns:
            Vector2D: Hasil pengurangan kedua vektor
            
        Note:
            v3 = other - self (bukan self - other)
        """
        return Vector2D(dx=other.dx - self.dx, dy=other.dy - self.dy)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        """
        Melakukan perkalian vektor dengan skalar (vektor * skalar).
        
        Args:
            scalar: Nilai pengali
            
        Returns:
            Vector2D: Hasil perkalian vektor dengan skalar
            
        Note:
            Mengimplementasikan operasi v * s dimana v adalah vektor dan s adalah skalar
        """
        return Vector2D(dx=self.dx * scalar, dy=self.dy * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector2D':
        """
        Melakukan perkalian vektor dengan skalar (skalar * vektor).
        
        Args:
            scalar: Nilai pengali
            
        Returns:
            Vector2D: Hasil perkalian vektor dengan skalar
            
        Note:
            Mengimplementasikan operasi s * v dimana s adalah skalar dan v adalah vektor
        """
        return Vector2D(dx=self.dx * scalar, dy=self.dy * scalar)
    
    @property
    def magnitude(self) -> float:
        """
        Menghitung panjang (magnitude) dari vektor.
        
        Returns:
            float: Panjang vektor
            
        Note:
            Menggunakan rumus |v| = sqrt(dx² + dy²)
        """
        return sqrt(self.dx * self.dx + self.dy * self.dy)
    
    @property
    def normal(self) -> 'Vector2D':
        """
        Menghitung vektor normal (tegak lurus) dari vektor ini.
        
        Returns:
            Vector2D: Vektor normal
            
        Note:
            Vektor normal dihitung dengan menukar komponen x dan y
            dan mengubah tanda salah satu komponen:
            normal.dx = -dy
            normal.dy = dx
        """
        return Vector2D(dx=-self.dy, dy=self.dx)
    
    @property
    def point(self) -> 'Site':
        """
        Mengkonversi vektor menjadi titik (Site).
        
        Returns:
            Site: Titik dengan koordinat (x,y) sama dengan komponen vektor (dx,dy)
            
        Note:
            Import Site dilakukan di dalam method untuk menghindari
            circular import
        """
        from Site import Site
        return Site(x=self.dx, y=self.dy)
