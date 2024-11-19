from typing import Optional, List
from weakref import ref, ReferenceType
from Beachline import Arc
from Site import Site
from LineSegment import LineSegment

Vertex = Site

class HalfEdge:
    """
    half-edge menyimpan pointer ke:
    - Origin(e)
    - Twin of e
    - Face sebelah kirinya (IncidentFace(e))
    - Next(e): half-edge berikutnya pada batas IncidentFace(e)
    - Previous(e): half-edge sebelumnya pada batas IncidentFace(e)
    """
    def __init__(self):
        self.origin: Optional[Vertex] = None
        self.destination: Optional[Vertex] = None
        
        # Menggunakan weak references untuk referensi siklik
        self._twin: Optional[ReferenceType[HalfEdge]] = None
        self._incident_face: Optional[ReferenceType[Cell]] = None
        self._prev: Optional[ReferenceType[HalfEdge]] = None
        self.next: Optional[HalfEdge] = None
    
    @property
    def twin(self) -> Optional['HalfEdge']:
        return self._twin() if self._twin is not None else None
    
    @twin.setter
    def twin(self, value: Optional['HalfEdge']):
        self._twin = ref(value) if value is not None else None
    
    @property
    def incident_face(self) -> Optional['Cell']:
        return self._incident_face() if self._incident_face is not None else None
    
    @incident_face.setter
    def incident_face(self, value: Optional['Cell']):
        self._incident_face = ref(value) if value is not None else None
    
    @property
    def prev(self) -> Optional['HalfEdge']:
        return self._prev() if self._prev is not None else None
    
    @prev.setter
    def prev(self, value: Optional['HalfEdge']):
        self._prev = ref(value) if value is not None else None
    
    def to_segment(self) -> Optional[LineSegment]:
        """Mengembalikan representasi line segment dari half-edge"""
        if self.origin is None or self.destination is None:
            return None
        return LineSegment(a=self.origin, b=self.destination)

class Cell:
    """
    Menyimpan pointer ke outerComponent linked list dan site
    """
    def __init__(self, site: Site):
        self.outer_component: Optional[HalfEdge] = None
        self.site: Site = site
    
    def __del__(self):
        """Membersihkan referensi siklik"""
        if self.outer_component:
            self.outer_component.next = None
            self.outer_component.prev = None
    
    def hull_vertices_ccw(self) -> List[Vertex]:
        """Mengembalikan vertex sel dalam urutan berlawanan arah jarum jam"""
        vertices = []
        if not self.outer_component:
            return vertices
        
        he = self.outer_component
        while True:
            if he.origin:
                vertices.append(he.origin)
            he = he.next
            if not he or he is self.outer_component:
                break
        
        return vertices
    
    def neighbours(self) -> List['Cell']:
        """Mengembalikan semua sel tetangga dari sel tertentu"""
        neighbours = []
        if not self.outer_component:
            return neighbours
        
        he = self.outer_component
        while True:
            if he.twin and he.twin.incident_face:
                neighbours.append(he.twin.incident_face)
            he = he.next
            if not he or he is self.outer_component:
                break
        
        return neighbours

class Diagram:
    """Kelas utama untuk menyimpan struktur diagram Voronoi"""
    def __init__(self):
        self.cells: List[Cell] = []
        self.vertices: List[Vertex] = []
    
    def create_cell(self, arc: 'Arc') -> None:
        """Membuat sel baru untuk busur yang diberikan"""
        if arc.point is None:
            return
        cell = Cell(site=arc.point)
        self.cells.append(cell)
        arc.cell = cell
    
    def create_half_edge(self, cell: Cell) -> HalfEdge:
        """Membuat half-edge baru yang terkait dengan sel yang diberikan"""
        he = HalfEdge()
        if cell.outer_component is None:
            cell.outer_component = he
        he.incident_face = cell
        return he
    
    def clear(self) -> None:
        """Menghapus semua sel dan vertex dari diagram"""
        self.cells.clear()
        self.vertices.clear()
