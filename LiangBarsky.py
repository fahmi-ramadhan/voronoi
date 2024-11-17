from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, NamedTuple
from LineSegment import LineSegment
from Site import Site

class LiangBarskyResult(NamedTuple):
    """
    Kelas untuk menyimpan hasil dari algoritma pemotongan Liang-Barsky.
    
    Attributes:
        is_origin_clipped: Menandakan apakah titik awal garis terpotong
        is_destination_clipped: Menandakan apakah titik akhir garis terpotong
        result_segment: Segmen garis hasil pemotongan, bernilai None jika garis sepenuhnya di luar area
    """
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
    """
    Kelas yang mendefinisikan persegi panjang pembatas untuk proses pemotongan.
    """
    left: float
    right: float
    top: float
    bottom: float

def lb_clip(line: LineSegment, clipper: Clipper) -> LiangBarskyResult:
    """
    Implementasi algoritma pemotongan garis Liang-Barsky.
    
    Fungsi ini memotong sebuah segmen garis terhadap persegi panjang pembatas
    menggunakan algoritma Liang-Barsky. Algoritma ini menghitung parameter t0 dan t1
    yang menentukan bagian garis yang berada di dalam area pembatas.
    
    Args:
        line: Objek LineSegment yang merepresentasikan garis yang akan dipotong
        clipper: Objek Clipper yang mendefinisikan persegi panjang pembatas
    
    Returns:
        LiangBarskyResult yang berisi informasi hasil pemotongan:
        - is_origin_clipped: True jika titik awal garis terpotong
        - is_destination_clipped: True jika titik akhir garis terpotong
        - result_segment: Segmen garis hasil pemotongan, None jika garis di luar area
    
    Referensi:
        - Implementasi Liang-Barsky oleh Daniel White:
          http://www.skytopia.com/project/articles/compsci/clipping.html
    """
    t0 = 0.0  # Parameter awal garis
    t1 = 1.0  # Parameter akhir garis
    
    # Menghitung perbedaan koordinat x dan y
    dx = line.b.x - line.a.x
    dy = line.b.y - line.a.y
    
    # Penanda apakah titik awal dan akhir terpotong
    is_origin_clipped = False
    is_destination_clipped = False
    
    # Iterasi untuk setiap sisi persegi pembatas
    for edge in ClipperEdge:
        # Menghitung parameter p dan q berdasarkan sisi yang diproses
        if edge == ClipperEdge.LEFT:
            p = -dx
            q = -(clipper.left - line.a.x)
        elif edge == ClipperEdge.RIGHT:
            p = dx
            q = (clipper.right - line.a.x)
        elif edge == ClipperEdge.BOTTOM:
            p = -dy
            q = -(clipper.bottom - line.a.y)
        else:  # TOP
            p = dy
            q = (clipper.top - line.a.y)
        
        # Kasus khusus: garis sejajar dengan sisi dan di luar area
        if p == 0 and q < 0:
            return LiangBarskyResult(False, False, None)
        
        if p != 0:
            r = q / p  # Menghitung parameter potong
            
            if p < 0:
                if r > t1:
                    # Garis sepenuhnya di luar area
                    return LiangBarskyResult(False, False, None)
                elif r > t0:
                    # Titik awal terpotong
                    is_origin_clipped = True
                    t0 = r
            elif p > 0:
                if r < t0:
                    # Garis sepenuhnya di luar area
                    return LiangBarskyResult(False, False, None)
                elif r < t1:
                    # Titik akhir terpotong
                    is_destination_clipped = True
                    t1 = r
    
    # Menghitung koordinat titik-titik hasil pemotongan
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
