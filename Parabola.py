import math
from Site import Site

class Parabola:
    """
    Kelas yang merepresentasikan parabola dalam diagram Voronoi.
    
    Parabola didefinisikan oleh titik fokus dan garis direktriks yang sejajar dengan sumbu X.
    Kelas ini menyediakan metode untuk:
    - Mengkonversi ke bentuk standar parabola
    - Menghitung nilai y untuk x tertentu
    - Mengkonversi ke kurva Bezier kuadratik
    - Menghitung titik perpotongan dengan parabola lain
    """
    
    def __init__(self, focus: Site, directrix_y: float):
        """
        Konstruktor untuk membuat parabola dengan titik fokus dan direktriks.
        
        Args:
            focus: Titik fokus parabola
            directrix_y: Koordinat y dari garis direktriks yang sejajar sumbu X
            
        Note:
            Garis direktriks harus sejajar dengan sumbu X untuk algoritma Fortune
        """
        self.focus = focus
        self.directrix_y = directrix_y
    
    @property
    def standard_form(self) -> tuple[float, float, float]:
        """
        Mengkonversi parabola ke bentuk standar (ax² + bx + c).
        
        Proses konversi:
        1. Menghitung koordinat vertex parabola (vx, vy)
        2. Menggunakan vertex untuk menghitung koefisien a, b, dan c
        
        Returns:
            Tuple berisi koefisien (a, b, c) dari persamaan parabola
        """
        # Koordinat x dari vertex parabola
        vx = self.focus.x 
        # Koordinat y dari vertex parabola
        vy = (self.focus.y + self.directrix_y) / 2

        # Jarak dari vertex ke fokus
        p = self.focus.y - vy
        
        # Parabola equation: (x - vx)^2 = 4p(y - vy)
        a = 1 / (4 * p)
        b = -2 * vx / (4 * p)
        c = (vx ** 2) / (4 * p) + vy
        
        return (a, b, c)
    
    def intersection_x(self, parabola: 'Parabola') -> float | None:
        """
        Menghitung koordinat x dari perpotongan dengan parabola lain.
        
        Metode ini menangani beberapa kasus:
        1. Kasus degenerasi ketika dua parabola memiliki y yang sama
        2. Kasus degenerasi ketika fokus memiliki y sama dengan direktriks
        3. Kasus umum menggunakan persamaan kuadrat
        
        Args:
            parabola: Parabola lain yang akan dicari titik perpotongannya
            
        Returns:
            Koordinat x titik perpotongan, atau None jika tidak ada perpotongan
            
        Note:
            Untuk kasus degenerasi, titik perpotongan berada tepat di tengah
            antara kedua fokus parabola
        """
        focus_left = self.focus
        focus_right = parabola.focus
        directrix = self.directrix_y
        
        # Tangani kasus degenerasi ketika dua parabola memiliki y yang sama
        if focus_left.y == focus_right.y:
            return (focus_left.x + focus_right.x) / 2
        
        # Tangani kasus degenerasi ketika fokus memiliki y sama dengan direktriks
        if focus_left.y == directrix:
            return focus_left.x
        elif focus_right.y == directrix:
            return focus_right.x
            
        # Tentukan koefisien a, b, dan c untuk kedua parabola
        a1, b1, c1 = self.standard_form
        a2, b2, c2 = parabola.standard_form
        
        # Hitung akar dari selisih koefisien
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2
        
        discriminant = b * b - 4 * a * c
        
        try:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            
            # Koordinat x perpotongan adalah salah satu dari akar tersebut
            x = min(x1, x2) if focus_left.y < focus_right.y else max(x1, x2)
            
            return None if math.isnan(x) else x
            
        except (ValueError, ZeroDivisionError):
            return None
