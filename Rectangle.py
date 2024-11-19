from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple, Optional, Dict
from LiangBarsky import Clipper
from Site import Site
from Site import Vector2D
from LineSegment import LineSegment

class RectangleEdge(Enum):
    TOP = auto()
    RIGHT = auto()
    LEFT = auto()
    BOTTOM = auto()

@dataclass
class Rectangle:
    """
    Kelas yang merepresentasikan persegi panjang dalam ruang 2D.
    
    Persegi panjang didefinisikan oleh titik origin (pojok kiri atas) 
    dan ukurannya (lebar dan tinggi).
    
    Attributes:
        x (float): Koordinat x dari titik origin
        y (float): Koordinat y dari titik origin
        width (float): Lebar persegi panjang
        height (float): Tinggi persegi panjang
    """
    x: float
    y: float
    width: float
    height: float
    
    @property
    def tl(self) -> 'Site':
        """Mendapatkan titik pojok kiri atas."""
        return Site(x=self.x, y=self.y)
    
    @property
    def bl(self) -> 'Site':
        """Mendapatkan titik pojok kiri bawah."""
        return Site(x=self.tl.x, y=self.tl.y + self.height)
    
    @property
    def tr(self) -> 'Site':
        """Mendapatkan titik pojok kanan atas."""
        return Site(x=self.tl.x + self.width, y=self.tl.y)
    
    @property
    def br(self) -> 'Site':
        """Mendapatkan titik pojok kanan bawah."""
        return Site(x=self.tl.x + self.width, y=self.tl.y + self.height)
    
    @property
    def origin(self) -> 'Site':
        """Mendapatkan titik origin (pojok kiri atas)."""
        return self.tl
    
    def expand_to_contain_point(self, p: 'Site', padding: float = 20.0) -> None:
        """
        Memperluas persegi panjang untuk mencakup titik yang diberikan.
        
        Args:
            p: Titik yang akan dicakup
            padding: Jarak tambahan dari titik ke tepi persegi panjang
        """
        if p.x <= self.origin.x:
            self.width += abs(self.x - p.x + padding)
            self.x = p.x - padding
        
        if p.y <= self.origin.y:
            self.height += abs(self.y - p.y + padding)
            self.y = p.y - padding
        
        if p.x >= self.origin.x + self.width:
            self.width = p.x - self.x + padding
        
        if p.y >= self.origin.y + self.height:
            self.height = p.y - self.y + padding
    
    def get_line(self, edge: RectangleEdge) -> LineSegment:
        """
        Mendapatkan segmen garis untuk sisi yang ditentukan.
        
        Args:
            edge: Sisi persegi panjang yang diinginkan
            
        Returns:
            Segmen garis yang merepresentasikan sisi
        """
        if edge == RectangleEdge.TOP:
            return LineSegment(a=self.tr, b=self.tl)
        elif edge == RectangleEdge.RIGHT:
            return LineSegment(a=self.br, b=self.tr)
        elif edge == RectangleEdge.BOTTOM:
            return LineSegment(a=self.bl, b=self.br)
        elif edge == RectangleEdge.LEFT:
            return LineSegment(a=self.tl, b=self.bl)
    
    @classmethod
    def rect_from_source(cls, source_rect: 'Rectangle', padding: float) -> 'Rectangle':
        """
        Membuat persegi panjang baru dengan padding dari persegi panjang sumber.
        
        Args:
            source_rect: Persegi panjang sumber
            padding: Jarak padding yang akan ditambahkan ke semua sisi
            
        Returns:
            Instance Rectangle baru yang lebih besar
        """
        return cls(
            x=source_rect.tl.x - padding,
            y=source_rect.tl.y - padding,
            width=source_rect.width + 2 * padding,
            height=source_rect.height + 2 * padding
        )
    
    def contains(self, point: Optional['Site']) -> bool:
        """
        Memeriksa apakah suatu titik berada di dalam persegi panjang.
        
        Args:
            point: Titik yang akan diperiksa
            
        Returns:
            True jika titik berada di dalam persegi panjang, False jika tidak
        """
        if point is None:
            return False
        return (point.x >= self.tl.x and point.x <= self.tr.x and 
                point.y >= self.tl.y and point.y <= self.br.y)
    
    def intersection(self, origin: 'Site', direction: 'Vector2D') -> Tuple['Site', RectangleEdge]:
        """
        Menghitung titik perpotongan garis dengan persegi panjang.
        
        Args:
            origin: Titik awal garis
            direction: Vektor arah garis
            
        Returns:
            Tuple berisi titik perpotongan dan sisi yang dipotong
            
        Raises:
            AssertionError: Jika tidak ditemukan perpotongan
        """
        point: Optional['Site'] = None
        edge: Optional[RectangleEdge] = None
        t = float('inf')
        
        if direction.dx > 0.0:
            right = self.get_line(RectangleEdge.RIGHT)
            t = (right.a.x - origin.x) / direction.dx
            point = (origin.vector + t * direction).point
            edge = RectangleEdge.RIGHT
        elif direction.dx < 0.0:
            left = self.get_line(RectangleEdge.LEFT)
            t = (left.a.x - origin.x) / direction.dx
            point = (origin.vector + t * direction).point
            edge = RectangleEdge.LEFT
            
        if direction.dy > 0.0:
            bottom = self.get_line(RectangleEdge.BOTTOM)
            new_t = (bottom.a.y - origin.y) / direction.dy
            if new_t < t:
                point = (origin.vector + new_t * direction).point
                edge = RectangleEdge.BOTTOM
        elif direction.dy < 0.0:
            top = self.get_line(RectangleEdge.TOP)
            new_t = (top.a.y - origin.y) / direction.dy
            if new_t < t:
                point = (origin.vector + new_t * direction).point
                edge = RectangleEdge.TOP
        
        assert point is not None and edge is not None
        return point, edge
    
    def _get_next_ccw(self, edge: RectangleEdge) -> Tuple[RectangleEdge, 'Site']:
        """
        Mendapatkan sisi dan titik pojok berikutnya dalam urutan berlawanan arah jarum jam.
        
        Args:
            edge: Sisi saat ini
            
        Returns:
            Tuple berisi sisi berikutnya dan titik pojok berikutnya
        """
        if edge == RectangleEdge.LEFT:
            return (RectangleEdge.BOTTOM, self.bl)
        elif edge == RectangleEdge.BOTTOM:
            return (RectangleEdge.RIGHT, self.br)
        elif edge == RectangleEdge.RIGHT:
            return (RectangleEdge.TOP, self.tr)
        elif edge == RectangleEdge.TOP:
            return (RectangleEdge.LEFT, self.tl)
            
    def side_for_point(self, p: 'Site') -> Optional[RectangleEdge]:
        """
        Menentukan pada sisi mana suatu titik berada.
        
        Args:
            p: Titik yang akan diperiksa
            
        Returns:
            Sisi di mana titik berada, atau None jika titik tidak berada pada sisi mana pun
        """
        segments: Dict[RectangleEdge, LineSegment] = {
            RectangleEdge.TOP: self.get_line(RectangleEdge.TOP),
            RectangleEdge.RIGHT: self.get_line(RectangleEdge.RIGHT),
            RectangleEdge.BOTTOM: self.get_line(RectangleEdge.BOTTOM),
            RectangleEdge.LEFT: self.get_line(RectangleEdge.LEFT)
        }
        
        for edge, segment in segments.items():
            if segment.contains_point(p):
                return edge
        return None
    
    def ccw_traverse(self, start_edge: RectangleEdge, end_edge: RectangleEdge) -> List['Site']:
        """
        Melakukan traversal titik-titik pojok dari sisi awal ke sisi akhir berlawanan arah jarum jam.
        
        Args:
            start_edge: Sisi awal traversal
            end_edge: Sisi akhir traversal
            
        Returns:
            List titik-titik pojok yang dilewati
        """
        points = []
        edge = start_edge
        while edge != end_edge:
            next_edge, point = self._get_next_ccw(edge)
            edge = next_edge
            points.append(point)
        return points
    
    def get_rect_polyline_for_ccw(self, start: 'Site', end: 'Site') -> List['Site']:
        """
        Mendapatkan polyline yang menghubungkan dua titik pada persegi panjang berlawanan arah jarum jam.
        
        Args:
            start: Titik awal pada persegi panjang
            end: Titik akhir pada persegi panjang
            
        Returns:
            List titik-titik yang membentuk polyline
        """
        result = []
        start_edge = self.side_for_point(start)
        end_edge = self.side_for_point(end)
        
        if start_edge is None or end_edge is None:
            return result
            
        if start_edge == end_edge:
            segment = self.get_line(start_edge)
            if segment.a.distance_to(start) < segment.a.distance_to(end):
                result = []
            else:
                next_edge, corner = self._get_next_ccw(start_edge)
                result.append(corner)
                result.extend(self.ccw_traverse(next_edge, start_edge))
        else:
            result.extend(self.ccw_traverse(start_edge, end_edge))
        return result
    
    def to_clipper(self) -> Clipper:
        """
        Mengkonversi persegi panjang ke objek Clipper untuk clipping.
        
        Returns:
            Objek Clipper yang merepresentasikan persegi panjang
        """
        return Clipper(
            left=self.tl.x,
            right=self.tr.x,
            top=self.tr.y,
            bottom=self.br.y
        )
