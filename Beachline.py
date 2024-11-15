from Parabola import Parabola

class Arc:
    def __init__(self, point=None):
        self.is_black = True
        self.point = point
        self.event = None
        self.prev = None
        self.next = None
        
        self.left_half_edge = None
        self.right_half_edge = None
        self.cell = None
        
        # Red-black tree properties
        self.right = None
        self.left = None
        self.parent = None

    def bounds(self, directrix_y):
        """Calculate the bounds of the arc"""
        l_bound = float('-inf')
        r_bound = float('inf')
        
        parabola = Parabola(focus=self.point, directrix_y=directrix_y)
        
        if self.prev:
            l_parabola = Parabola(focus=self.prev.point, directrix_y=directrix_y)
            intersection_x = l_parabola.intersection_x(parabola)
            if intersection_x is not None:
                l_bound = intersection_x
        
        if self.next:
            r_parabola = Parabola(focus=self.next.point, directrix_y=directrix_y)
            intersection_x = parabola.intersection_x(r_parabola)
            if intersection_x is not None:
                r_bound = intersection_x
        
        return (l_bound, r_bound)

class Beachline:
    def __init__(self):
        self.sweepline_y = 0
        self.sentinel = Arc()
        self.root = None
        
    def _minimum(self, x):
        while x.left is not self.sentinel:
            x = x.left
        return x
    
    def _maximum(self, x):
        while x.right is not self.sentinel:
            x = x.right
        return x
    
    def _transplant(self, u, v):
        if u.parent is self.sentinel:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        elif u is u.parent.right:
            u.parent.right = v
        v.parent = u.parent

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        
        if y.left is not self.sentinel:
            y.left.parent = x
        y.parent = x.parent
        
        if x.parent is self.sentinel:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        elif x is x.parent.right:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        
        if y.right is not self.sentinel:
            y.right.parent = x
        y.parent = x.parent
        
        if x.parent is self.sentinel:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        elif x is x.parent.left:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fixup(self, z):
        while not z.parent.is_black:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y and not y.is_black:
                    z.parent.is_black = True
                    y.is_black = True
                    z.parent.parent.is_black = False
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.is_black = True
                    z.parent.parent.is_black = False
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and not y.is_black:
                    z.parent.is_black = True
                    y.is_black = True
                    z.parent.parent.is_black = False
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.is_black = True
                    z.parent.parent.is_black = False
                    self._left_rotate(z.parent.parent)
        self.root.is_black = True

    def delete_fixup(self, x):
        while x is not self.root and x.is_black:
            if x is x.parent.left:
                w = x.parent.right
                if not w.is_black:
                    w.is_black = True
                    x.parent.is_black = False
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.is_black and w.right.is_black:
                    w.is_black = False
                    x = x.parent
                else:
                    if w.right.is_black:
                        w.left.is_black = True
                        w.is_black = False
                        self._right_rotate(w)
                        w = x.parent.right
                    w.is_black = x.parent.is_black
                    x.parent.is_black = True
                    w.right.is_black = True
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if not w.is_black:
                    w.is_black = True
                    x.parent.is_black = False
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.is_black and w.left.is_black:
                    w.is_black = False
                    x = x.parent
                else:
                    if w.left.is_black:
                        w.right.is_black = True
                        w.is_black = True
                        self._left_rotate(w)
                        w = x.parent.left
                    w.is_black = x.parent.is_black
                    x.parent.is_black = True
                    w.left.is_black = True
                    self._right_rotate(x.parent)
                    x = self.root
        x.is_black = True

    def delete(self, z):
        y = z
        y_original_color = y.is_black
        if z.left is self.sentinel:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.sentinel:
            x = z.left
            if z.left is not self.sentinel:
                self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.is_black
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.is_black = z.is_black
        if y_original_color:
            self.delete_fixup(x)

    @property
    def is_empty(self):
        return self.root is None

    def insert_root_arc(self, point):
        self.root = Arc(point=point)
        self.root.left = self.sentinel
        self.root.right = self.sentinel
        self.root.parent = self.sentinel
        self.root.is_black = True
        return self.root

    def update_sweepline_y(self, y):
        self.sweepline_y = y

    def add_as_left_child(self, x, y):
        y.left = x
        x.parent = y
        x.left = self.sentinel
        x.right = self.sentinel
        x.is_black = False
        self.insert_fixup(x)

    def add_as_right_child(self, x, y):
        y.right = x
        x.parent = y
        x.left = self.sentinel
        x.right = self.sentinel
        x.is_black = False
        self.insert_fixup(x)

    def insert_arc_for_point(self, p):
        eps = 1e-10  # Define small epsilon for floating point comparison
        mid = Arc(point=p)
        x = self.root
        found = False
        is_edge_case = False
        
        while not found:
            assert x.point is not None
            l, r = x.bounds(self.sweepline_y)
            if p.x < l:
                x = x.left
            elif p.x > r:
                x = x.right
            elif abs(p.x - l) < eps:
                self.insert_successor(x.prev, mid)
                is_edge_case = True
                found = True
            elif abs(p.x - r) < eps:
                self.insert_successor(x, mid)
                is_edge_case = True
                found = True
            else:
                self.insert_successor(x, mid)
                right = Arc(point=x.point)
                self.insert_successor(mid, right)
                is_edge_case = False
                found = True
        return mid, is_edge_case

    def handle_special_arc_insertion_case(self, p):
        arc = Arc(point=p)
        current = self.root
        found = False
        while not found:
            if current.next is not None:
                current = current.next
            else:
                found = True
        self.insert_successor(current, arc)
        return arc

    def insert_successor(self, p, s):
        s.prev = p
        s.next = p.next
        p.next = s
        if s.next:
            s.next.prev = s
        
        if p.right is self.sentinel:
            self.add_as_right_child(s, p)
        else:
            r = p.right
            while r.left is not self.sentinel:
                r = r.left
            self.add_as_left_child(s, r)

    def delete_arc(self, arc):
        prev = arc.prev
        next_arc = arc.next
        
        if prev:
            prev.next = next_arc
        if next_arc:
            next_arc.prev = prev
        
        self.delete(arc)

    @property
    def minimum(self):
        if self.root is self.sentinel or self.root is None:
            return None
        return self._minimum(self.root)

    @property
    def maximum(self):
        if self.root is self.sentinel or self.root is None:
            return None
        return self._maximum(self.root)