from dataclasses import dataclass, field
from typing import Any, Optional, List
from weakref import ref, ReferenceType
from Beachline import Arc
from Site import Site
from LineSegment import LineSegment

# Type aliases
Vertex = Site
Point = Site

class HalfEdge:
    """
    The half-edge record of a half-edge e stores pointers to:
    - Origin(e)
    - Twin of e
    - The face to its left (IncidentFace(e))
    - Next(e): next half-edge on the boundary of IncidentFace(e)
    - Previous(e): previous half-edge
    """
    def __init__(self):
        self.satellite: Any = None
        self.origin: Optional[Vertex] = None
        self.destination: Optional[Vertex] = None
        
        # Using weak references for cyclic references
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
        """Returns a line segment representation of the half-edge"""
        if self.origin is None or self.destination is None:
            return None
        return LineSegment(a=self.origin, b=self.destination)

class Cell:
    """
    Stores pointer to:
    - outerComponent linked list (looped when diagram is built)
    - site - pointer to the site
    """
    def __init__(self, site: Site):
        self.satellite: Any = None
        self.outer_component: Optional[HalfEdge] = None
        self.site: Site = site
    
    def __del__(self):
        """Clean up circular references"""
        if self.outer_component:
            self.outer_component.next = None
            self.outer_component.prev = None
    
    def hull_vertices_ccw(self) -> List[Vertex]:
        """Returns cell vertices in counter-clockwise order"""
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
        """Returns all the neighbours of specific cell"""
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
    """Main class for storing the Voronoi diagram structure"""
    def __init__(self):
        self.cells: List[Cell] = []
        self.vertices: List[Vertex] = []
    
    def create_cell(self, arc: 'Arc') -> None:
        """Creates a new cell for the given arc"""
        if arc.point is None:
            return
        cell = Cell(site=arc.point)
        self.cells.append(cell)
        arc.cell = cell
    
    def create_half_edge(self, cell: Cell) -> HalfEdge:
        """Creates a new half-edge associated with the given cell"""
        he = HalfEdge()
        if cell.outer_component is None:
            cell.outer_component = he
        he.incident_face = cell
        return he
    
    def clear(self) -> None:
        """Clears all cells and vertices from the diagram"""
        self.cells.clear()
        self.vertices.clear()