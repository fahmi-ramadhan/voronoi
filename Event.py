from enum import Enum
from dataclasses import dataclass
from typing import Optional
from Beachline import Arc
import Site
from Circle import Circle

class EventKind(Enum):
    SITE = "site"
    CIRCLE = "circle"

@dataclass
class Event:
    """
    Kelas yang merepresentasikan event dalam algoritma Fortune.
    
    Event adalah kejadian yang memicu perubahan dalam struktur beachline.
    Ada dua jenis event:
    1. Site event: Saat sweep line mencapai site baru
    2. Circle event: Saat tiga arc berpotongan membentuk vertex diagram Voronoi
    
    Attributes:
        point: Titik koordinat di mana event terjadi
        kind: Jenis event (SITE atau CIRCLE)
        arc: Arc yang terkait dengan circle event (hanya untuk circle event)
        circle: Lingkaran yang mendefinisikan circle event (hanya untuk circle event)
    """
    point: 'Site'
    kind: EventKind = EventKind.SITE
    # Atribut untuk circle event
    arc: Optional['Arc'] = None
    circle: Optional['Circle'] = None

    def __eq__(self, other: 'Event') -> bool:
        """
        Membandingkan kesamaan dua event.
        
        Events dianggap sama jika memiliki titik dan jenis yang sama.
        
        Args:
            other: Event lain yang akan dibandingkan
            
        Returns:
            bool: True jika kedua event sama, False jika berbeda
        """
        if not isinstance(other, Event):
            return NotImplemented
        return self.point == other.point and self.kind == other.kind

    def __lt__(self, other: 'Event') -> bool:
        """
        Membandingkan urutan dua event berdasarkan posisi y (prioritas utama)
        dan posisi x (prioritas kedua).
        
        Digunakan untuk mengurutkan event dalam priority queue berdasarkan:
        1. Posisi y (sweep line) - event dengan y lebih kecil diproses lebih dulu
        2. Jika y sama, bandingkan posisi x
        
        Args:
            other: Event lain yang akan dibandingkan
            
        Returns:
            bool: True jika self harus diproses sebelum other
        """
        if not isinstance(other, Event):
            return NotImplemented
        if self.point.y == other.point.y:
            return self.point.x < other.point.x
        return self.point.y < other.point.y
