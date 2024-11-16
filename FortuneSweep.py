from queue import PriorityQueue
from typing import Set, Optional, Tuple
from Beachline import Beachline, Arc
from Circle import Point, Circle
from Event import Event, EventKind
from Rectangle import Rectangle
from Diagram import Diagram, HalfEdge, Site, Cell
from LiangBarsky import lb_clip

class FortuneSweep:
    def __init__(self):
        self.event_queue = PriorityQueue()
        self.beachline = Beachline()
        self.sweep_line_y = 0
        self.first_site_y = None
        self.container = None
        self.clipper = None
        self.diagram = None
        self.current_step = 0
        self.is_terminated = False

    def compute(self, sites: Set[Point], diagram: Diagram, clipping_rect: Rectangle, max_steps_count: int = -1) -> bool:
        self.diagram = diagram
        self.clipper = clipping_rect
        
        # Filter sites within clipping rectangle
        filtered_sites = {site for site in sites if self.clipper.contains(site)}
        
        # Create events from sites
        events = [Event(point=site) for site in filtered_sites]
        
        # If no sites in clipping area, return True (done)
        if not events:
            return True
        
        # Initialize state
        self.current_step = 0
        self.sweep_line_y = 0
        self.first_site_y = None
        self.beachline = Beachline()
        
        # Set up priority queue
        for event in events:
            self.event_queue.put(event)
        
        self.is_terminated = False
        
        # Main loop
        while not self.event_queue.empty() and self.current_step != max_steps_count:
            self.step()
        
        if self.event_queue.empty():
            self.terminate()
            return True
        
        return False

    def step(self):
        if not self.event_queue.empty():
            event = self.event_queue.get()
            self.current_step += 1
            if event.kind == EventKind.SITE:
                self.process_site_event(event)
            else:
                self.process_circle_event(event)

    def process_site_event(self, event: Event):
        self.sweep_line_y = event.point.y
        self.beachline.update_sweepline_y(self.sweep_line_y)
        
        if self.beachline.is_empty:
            root = self.beachline.insert_root_arc(event.point)
            self.first_site_y = event.point.y
            self.container = Rectangle.rect_from_source(self.clipper, 20)
            self.container.expand_to_contain_point(event.point)
            self.diagram.create_cell(root)
            return
        
        if self.first_site_y == self.sweep_line_y:
            self.container.expand_to_contain_point(event.point)
            y_val = -1000000
            arc = self.beachline.handle_special_arc_insertion_case(event.point)
            self.diagram.create_cell(arc)
            prev = arc.prev
            p = Site(x=(prev.point.x + arc.point.x) / 2, y=y_val)
            prev.right_half_edge = self.diagram.create_half_edge(prev.cell)
            prev.right_half_edge.destination = p
            arc.left_half_edge = self.diagram.create_half_edge(arc.cell)
            arc.left_half_edge.origin = p
            self.make_twins(prev.right_half_edge, arc.left_half_edge)
            return
        
        new_arc, is_special_case = self.beachline.insert_arc_for_point(event.point)
        self.container.expand_to_contain_point(event.point)
        self.diagram.create_cell(new_arc)
        
        self.remove_circle_event(new_arc.prev)
        self.create_circle_event(new_arc.prev)
        self.create_circle_event(new_arc.next)
        
        next_arc = new_arc.next
        prev_arc = new_arc.prev
        
        if is_special_case:
            vertex = Circle.from_three_points(prev_arc.point, new_arc.point, next_arc.point).center
            prev_arc.right_half_edge.origin = vertex
            next_arc.left_half_edge.destination = vertex
            lhe = self.diagram.create_half_edge(new_arc.cell)
            new_arc.left_half_edge = lhe
            lhe.origin = vertex
            l_twin = self.diagram.create_half_edge(prev_arc.cell)
            l_twin.destination = vertex
            self.make_twins(lhe, l_twin)
            rhe = self.diagram.create_half_edge(new_arc.cell)
            new_arc.right_half_edge = rhe
            rhe.destination = vertex
            r_twin = self.diagram.create_half_edge(next_arc.cell)
            r_twin.origin = vertex
            self.make_twins(rhe, r_twin)
            self.connect(prev_arc.right_half_edge, lhe)
            self.connect(rhe, next_arc.left_half_edge)
            prev_arc.right_half_edge = l_twin
            next_arc.left_half_edge = r_twin
        else:
            next_arc.cell = prev_arc.cell
            next_arc.right_half_edge = prev_arc.right_half_edge
            prev_arc.right_half_edge = self.diagram.create_half_edge(prev_arc.cell)
            new_arc.left_half_edge = self.diagram.create_half_edge(new_arc.cell)
            self.make_twins(prev_arc.right_half_edge, new_arc.left_half_edge)
            new_arc.right_half_edge = new_arc.left_half_edge
            next_arc.left_half_edge = prev_arc.right_half_edge

    def process_circle_event(self, event: Event):
        arc = event.arc
        left = arc.prev
        right = arc.next
        center = event.circle.center
        
        self.sweep_line_y = event.point.y
        self.beachline.update_sweepline_y(self.sweep_line_y)
        
        self.beachline.delete_arc(arc)
        self.remove_circle_event(arc)
        self.remove_circle_event(left)
        self.remove_circle_event(right)
        
        self.create_vertex(center, arc)
        self.create_circle_event(left)
        self.create_circle_event(right)

    def create_vertex(self, vertex: Point, removed_arc: Arc):
        self.container.expand_to_contain_point(vertex)
        prev_arc = removed_arc.prev
        next_arc = removed_arc.next
        
        removed_arc.left_half_edge.destination = vertex
        removed_arc.right_half_edge.origin = vertex
        
        if prev_arc:
            prev_arc.right_half_edge.origin = vertex
            prev_arc.right_half_edge.twin.destination = vertex
        
        if next_arc:
            next_arc.left_half_edge.destination = vertex
            next_arc.left_half_edge.twin.origin = vertex
        
        if prev_arc and next_arc:
            self.connect(prev_arc.right_half_edge.twin, next_arc.left_half_edge.twin)
        
        if prev_arc:
            prev_rhe = self.diagram.create_half_edge(prev_arc.cell)
            prev_rhe.destination = vertex
            self.connect(prev_rhe, prev_arc.right_half_edge)
            prev_arc.right_half_edge = prev_rhe
        
        if next_arc:
            next_lhe = self.diagram.create_half_edge(next_arc.cell)
            next_lhe.origin = vertex
            self.connect(next_arc.left_half_edge, next_lhe)
            next_arc.left_half_edge = next_lhe
        
        if prev_arc and next_arc:
            self.make_twins(prev_arc.right_half_edge, next_arc.left_half_edge)

    def create_circle_event(self, arc: Arc):
        left = arc.prev
        right = arc.next
        circle = self.check_circle_event(left, arc, right)
        if circle:
            event = Event(point=circle.bottom_point, kind=EventKind.CIRCLE)
            event.circle = circle
            event.arc = arc
            arc.event = event
            self.event_queue.put(event)

    def remove_circle_event(self, arc: Optional[Arc]):
        if arc and arc.event and arc.event.kind == EventKind.CIRCLE:
            if arc.event in self.event_queue.queue:
                self.event_queue.queue.remove(arc.event)
            arc.event = None

    def terminate(self):
        self.is_terminated = True
        arc = self.beachline.minimum
        while arc:
            self.bound_incomplete_arc(arc)
            arc = arc.next
        
        min_arc = self.beachline.minimum
        max_arc = self.beachline.maximum
        
        if min_arc and max_arc and min_arc.cell == max_arc.cell:
            prev = max_arc.prev
            next_arc = min_arc.next
            if prev and next_arc:
                max_arc.left_half_edge.destination = self.get_box_intersection(prev.point, max_arc.point, self.container)
                min_arc.right_half_edge.origin = self.get_box_intersection(min_arc.point, next_arc.point, self.container)
                start = min_arc.right_half_edge.origin
                end = max_arc.left_half_edge.destination
                if start and end:
                    head, tail = self.half_edges_chain(max_arc.cell, self.container, end, start)
                    self.connect(max_arc.left_half_edge, head)
                    self.connect(tail, min_arc.right_half_edge)
        
        for cell in self.diagram.cells:
            if not cell.outer_component or not cell.outer_component.prev or not cell.outer_component.next:
                self.complete_incomplete_cell(cell)
            self.clip_cell(cell, self.clipper)

    def complete_incomplete_cell(self, cell: Cell):
        if not cell.outer_component:
            return
        first = cell.outer_component
        last = cell.outer_component
        
        while first.prev:
            first = first.prev
        
        while last.next:
            last = last.next
        
        clipper = self.container.to_clipper()
        last_segment = lb_clip(last.to_segment(), clipper)
        if last_segment and last_segment.result_segment:
            last.destination = last_segment.result_segment.b
        first_segment = lb_clip(first.to_segment(), clipper)
        if first_segment and first_segment.result_segment:
            first.origin = first_segment.result_segment.a
        
        start = last.destination
        end = first.origin
        if start and end:
            head, tail = self.half_edges_chain(cell, self.container, start, end)
            self.connect(last, head)
            self.connect(tail, first)

    def bound_incomplete_arc(self, arc: Arc):
        start_point = None
        end_point = None
        if arc.prev:
            start_point = self.get_box_intersection(arc.prev.point, arc.point, self.container)
            arc.prev.right_half_edge.origin = start_point
        
        if arc.next:
            end_point = self.get_box_intersection(arc.point, arc.next.point, self.container)
            arc.next.left_half_edge.destination = end_point
        
        if start_point and end_point:
            head, tail = self.half_edges_chain(arc.cell, self.container, start_point, end_point)
            self.connect(arc.left_half_edge, head)
            self.connect(tail, arc.right_half_edge)

    def clip_cell(self, cell: Cell, clipping_rect: Rectangle):
        if not cell.outer_component:
            corners = [clipping_rect.tl, clipping_rect.bl, clipping_rect.br, clipping_rect.tr]
            first_he = None
            for i in range(len(corners)):
                he = self.diagram.create_half_edge(cell)
                he.origin = corners[i - 1]
                he.destination = corners[i % len(corners)]
                if i == 0:
                    first_he = he
                    cell.outer_component = he
                self.connect(cell.outer_component, he)
                cell.outer_component = he
            self.connect(cell.outer_component, first_he)
            return
        
        he = cell.outer_component
        hes = []
        first_out = -1
        finish = False
        while not finish:
            segment_to_clip = he.to_segment()
            is_origin_clipped, is_destination_clipped, segment = lb_clip(segment_to_clip, clipping_rect.to_clipper())
            if is_origin_clipped or is_destination_clipped:
                if is_destination_clipped:
                    if first_out < 0:
                        first_out = len(hes)
                    he.destination = segment.b
                if is_origin_clipped:
                    he.origin = segment.a
                hes.append((he, is_origin_clipped, is_destination_clipped))
            he = he.next
            finish = he == cell.outer_component
        
        i = first_out
        while i < len(hes) + first_out:
            cur_idx = i % len(hes)
            next_idx = (i + 1) % len(hes)
            head, tail = self.half_edges_chain(cell, self.clipper, hes[cur_idx][0].destination, hes[next_idx][0].origin)
            self.connect(hes[cur_idx][0], head)
            self.connect(tail, hes[next_idx][0])
            if hes[next_idx][2]:
                i += 1
            else:
                i += 2

    def half_edges_chain(self, cell: Cell, clipping_rect: Rectangle, start: Site, end: Site) -> Tuple[HalfEdge, HalfEdge]:
        points = clipping_rect.get_rect_polyline_for_ccw(start, end)
        head = self.diagram.create_half_edge(cell)
        head.origin = start
        he = head
        for point in points:
            he.destination = point
            new_he = self.diagram.create_half_edge(cell)
            new_he.origin = point
            self.connect(he, new_he)
            he = new_he
        he.destination = end
        return head, he

    def get_box_intersection(self, p1: Site, p2: Site, rectangle: Rectangle) -> Site:
        intersection_point, _ = rectangle.intersection(
            origin=((p1.vector + p2.vector) * 0.5).point,
            direction=(p1.vector - p2.vector).normal
        )
        return intersection_point

    def make_twins(self, a: HalfEdge, b: HalfEdge):
        a.twin = b
        b.twin = a

    def connect(self, prev: HalfEdge, next: HalfEdge):
        prev.next = next
        next.prev = prev

    def check_circle_event(self, left: Optional[Arc], mid: Arc, right: Optional[Arc]) -> Optional[Circle]:
        if not left or not right:
            return None
        a = left.point
        b = mid.point
        c = right.point
        circle = Circle.from_three_points(a, b, c)
        if not circle:
            return None
        determinant = (b.x * c.y + a.x * b.y + a.y * c.x) - (a.y * b.x + b.y * c.x + a.x * c.y)
        event_y = circle.center.y + circle.radius
        if event_y >= self.sweep_line_y and determinant > 0:
            return circle
        return None
