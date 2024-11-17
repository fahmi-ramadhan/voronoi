from typing import Any, Optional
from dataclasses import dataclass
from Vector import Vector2D

@dataclass
class Site:
    """
    Kelas yang merepresentasikan titik atau lokasi dalam ruang 2D.
    
    Kelas ini menyediakan fungsionalitas untuk:
    - Menyimpan koordinat x dan y
    - Menghitung jarak antar titik
    - Konversi ke vektor 2D
    
    Attributes:
        x (float): Koordinat x dari titik
        y (float): Koordinat y dari titik
    """
    x: float
    y: float
    
    def __str__(self) -> str:
        """
        Menghasilkan representasi string dari titik.
        
        Returns:
            str: String dalam format "(x: {x}, y: {y})"
        """
        return f"(x: {self.x}, y: {self.y})"
    
    def __repr__(self) -> str:
        """
        Menghasilkan representasi string formal dari titik.
        Menggunakan format yang sama dengan __str__ untuk konsistensi.
        
        Returns:
            str: String dalam format "(x: {x}, y: {y})"
        """
        return self.__str__()
    
    def __eq__(self, other: 'Site') -> bool:
        """
        Membandingkan kesamaan dengan titik lain.
        Dua titik dianggap sama jika koordinat x dan y mereka sama.
        
        Args:
            other: Titik lain yang akan dibandingkan
            
        Returns:
            bool: True jika kedua titik sama, False jika tidak
            NotImplemented: Jika other bukan instance dari Site
        """
        if not isinstance(other, Site):
            return NotImplemented
        return (self.x == other.x and 
                self.y == other.y)
    
    def __hash__(self) -> int:
        """
        Menghasilkan nilai hash untuk titik.
        Hash didasarkan pada tuple koordinat (x, y).
        
        Returns:
            int: Nilai hash unik untuk titik ini
        
        Note:
            Diimplementasikan untuk mendukung penggunaan Site sebagai
            key dalam dict atau elemen dalam set
        """
        return hash((self.x, self.y))
    
    @property
    def vector(self) -> Vector2D:
        """
        Mengkonversi titik menjadi vektor 2D.
        
        Returns:
            Vector2D: Vektor dengan komponen x dan y yang sama dengan titik ini
        
        Note:
            Vektor yang dihasilkan memiliki titik awal di origin (0,0)
            dan mengarah ke titik ini
        """
        return Vector2D(dx=self.x, dy=self.y)
    
    def distance_to(self, point: 'Site') -> float:
        """
        Menghitung jarak Euclidean ke titik lain.
        
        Args:
            point: Titik tujuan yang akan dihitung jaraknya
            
        Returns:
            float: Jarak Euclidean antara kedua titik
        
        Note:
            Menggunakan rumus jarak Euclidean:
            distance = sqrt((x2-x1)² + (y2-y1)²)
        """
        x_dist = self.x - point.x
        y_dist = self.y - point.y
        return (x_dist * x_dist + y_dist * y_dist) ** 0.5
