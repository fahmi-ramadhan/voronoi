from dataclasses import dataclass
from math import sqrt

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
    def vector(self) -> 'Vector2D':
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
        """
        return Site(x=self.dx, y=self.dy)
