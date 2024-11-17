from Parabola import Parabola
from Precision import eps

class Arc:
    """
    Kelas yang merepresentasikan busur parabolik pada beachline.
    Menggunakan properti red-black tree untuk menjaga keseimbangan struktur data.
    """
    def __init__(self, point=None):
        """
        Inisialisasi arc baru.
        
        Args:
            point: Titik fokus dari parabola (titik pada diagram Voronoi)
        """
        # Properti Red-Black Tree
        self.is_black = True
        self.right = None
        self.left = None
        self.parent = None
        
        # Properti Geometris
        self.point = point
        self.event = None  # Event yang terkait dengan arc ini
        self.prev = None   # Arc sebelumnya dalam urutan beachline
        self.next = None   # Arc setelahnya dalam urutan beachline
        
        # Properti Diagram Voronoi
        self.left_half_edge = None  # Half-edge kiri dari cell Voronoi
        self.right_half_edge = None # Half-edge kanan dari cell Voronoi
        self.cell = None            # Cell Voronoi yang terkait dengan arc

    def bounds(self, directrix_y):
        """
        Menghitung batasan x dari arc pada posisi sweep line tertentu.
        
        Args:
            directrix_y: Posisi y dari sweep line
            
        Returns:
            tuple: (batas_kiri, batas_kanan) dari arc
        """
        l_bound = float('-inf')
        r_bound = float('inf')
        
        parabola = Parabola(focus=self.point, directrix_y=directrix_y)
        
        # Hitung intersection dengan arc sebelumnya untuk batas kiri
        if self.prev:
            l_parabola = Parabola(focus=self.prev.point, directrix_y=directrix_y)
            intersection_x = l_parabola.intersection_x(parabola)
            if intersection_x is not None:
                l_bound = intersection_x
        
        # Hitung intersection dengan arc berikutnya untuk batas kanan
        if self.next:
            r_parabola = Parabola(focus=self.next.point, directrix_y=directrix_y)
            intersection_x = parabola.intersection_x(r_parabola)
            if intersection_x is not None:
                r_bound = intersection_x
        
        return (l_bound, r_bound)

class Beachline:
    """
    Implementasi beachline menggunakan Red-Black Tree.
    Beachline menyimpan urutan arc parabolik yang terbentuk saat sweep line bergerak.
    """
    def __init__(self):
        """Inisialisasi beachline kosong."""
        self.sweepline_y = 0
        self.sentinel = Arc()  # Node sentinel untuk Red-Black Tree
        self.root = None
        
    def _minimum(self, x):
        """Mencari node dengan nilai minimum dalam subtree."""
        while x.left is not self.sentinel:
            x = x.left
        return x
    
    def _maximum(self, x):
        """Mencari node dengan nilai maksimum dalam subtree."""
        while x.right is not self.sentinel:
            x = x.right
        return x
    
    def _transplant(self, u, v):
        """
        Mengganti subtree yang berakar di u dengan subtree yang berakar di v.
        
        Args:
            u: Root dari subtree yang akan diganti
            v: Root dari subtree pengganti
        """
        if u.parent is self.sentinel:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        elif u is u.parent.right:
            u.parent.right = v
        v.parent = u.parent

    def _left_rotate(self, x):
        """
        Melakukan rotasi kiri pada node x.
        
        Args:
            x: Node yang akan dirotasi
        """
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
        """
        Melakukan rotasi kanan pada node x.
        
        Args:
            x: Node yang akan dirotasi
        """
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
        """
        Memperbaiki properti Red-Black Tree setelah penyisipan.
        
        Args:
            z: Node yang baru disisipkan
        """
        while not z.parent.is_black:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y and not y.is_black:
                    # Kasus 1: Uncle berwarna merah
                    z.parent.is_black = True
                    y.is_black = True
                    z.parent.parent.is_black = False
                    z = z.parent.parent
                else:
                    # Kasus 2 & 3: Uncle berwarna hitam
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.is_black = True
                    z.parent.parent.is_black = False
                    self._right_rotate(z.parent.parent)
            else:
                # Sama dengan kasus di atas tapi dengan arah yang berlawanan
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
        """
        Memperbaiki properti Red-Black Tree setelah penghapusan.
        
        Args:
            x: Node pengganti dari node yang dihapus
        """
        while x is not self.root and x.is_black:
            if x is x.parent.left:
                w = x.parent.right
                if not w.is_black:
                    # Kasus 1: Sibling berwarna merah
                    w.is_black = True
                    x.parent.is_black = False
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.is_black and w.right.is_black:
                    # Kasus 2: Kedua anak sibling berwarna hitam
                    w.is_black = False
                    x = x.parent
                else:
                    # Kasus 3 & 4: Setidaknya satu anak sibling berwarna merah
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
                # Sama dengan kasus di atas tapi dengan arah yang berlawanan
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
        """
        Menghapus node dari Red-Black Tree.
        
        Args:
            z: Node yang akan dihapus
        """
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
        """Mengecek apakah beachline kosong."""
        return self.root is None

    def insert_root_arc(self, point):
        """
        Menyisipkan arc pertama ke beachline kosong.
        
        Args:
            point: Titik fokus dari arc
            
        Returns:
            Arc: Arc yang baru disisipkan
        """
        self.root = Arc(point=point)
        self.root.left = self.sentinel
        self.root.right = self.sentinel
        self.root.parent = self.sentinel
        self.root.is_black = True
        return self.root

    def update_sweepline_y(self, y):
        """
        Memperbarui posisi y dari sweep line.
        
        Args:
            y: Posisi y baru dari sweep line
        """
        self.sweepline_y = y

    def add_as_left_child(self, x, y):
        """
        Menambahkan node sebagai anak kiri.
        
        Args:
            x: Node yang akan ditambahkan
            y: Node parent
        """
        y.left = x
        x.parent = y
        x.left = self.sentinel
        x.right = self.sentinel
        x.is_black = False
        self.insert_fixup(x)

    def add_as_right_child(self, x, y):
        """
        Menambahkan node sebagai anak kanan.
        
        Args:
            x: Node yang akan ditambahkan
            y: Node parent
        """
        y.right = x
        x.parent = y
        x.left = self.sentinel
        x.right = self.sentinel
        x.is_black = False
        self.insert_fixup(x)

    def insert_arc_for_point(self, p):
        """
        Menyisipkan arc baru untuk titik tertentu dengan menangani beberapa edge case:
        1. Ketika titik baru tepat berada di breakpoint (intersection) antara dua arc
        2. Ketika titik baru berada di luar batas kiri/kanan arc yang ada
        
        Args:
            p: Titik fokus untuk arc baru
            
        Returns:
            tuple: (arc_baru, is_edge_case) 
                   is_edge_case = True jika titik berada di breakpoint
        """
        mid = Arc(point=p)  # Arc baru yang akan disisipkan
        x = self.root
        found = False
        is_edge_case = False
        
        while not found:
            assert x.point is not None
            l, r = x.bounds(self.sweepline_y)  # Dapatkan batas kiri dan kanan dari arc saat ini
            
            # Edge Case 1: Titik berada di luar batas
            if p.x < l:
                # Titik berada di sebelah kiri arc - lanjut ke subtree kiri
                x = x.left
            elif p.x > r:
                # Titik berada di sebelah kanan arc - lanjut ke subtree kanan
                x = x.right
                
            # Edge Case 2: Titik tepat berada di breakpoint kiri
            elif abs(p.x - l) < eps:
                # Titik berada di intersection dengan arc sebelumnya
                # Sisipkan setelah arc sebelumnya
                self.insert_successor(x.prev, mid)
                is_edge_case = True
                found = True
                
            # Edge Case 3: Titik tepat berada di breakpoint kanan
            elif abs(p.x - r) < eps:
                # Titik berada di intersection dengan arc berikutnya
                # Sisipkan setelah arc saat ini
                self.insert_successor(x, mid)
                is_edge_case = True
                found = True
                
            # Kasus Normal: Titik berada di dalam arc yang ada
            else:
                # Arc yang ada dibagi menjadi tiga bagian:
                # 1. Arc kiri (arc yang ada)
                # 2. Arc tengah (arc baru)
                # 3. Arc kanan (copy dari arc yang ada)
                self.insert_successor(x, mid)
                right = Arc(point=x.point)
                self.insert_successor(mid, right)
                is_edge_case = False
                found = True
                
        return mid, is_edge_case

    def handle_special_arc_insertion_case(self, p):
        """
        Menangani kasus khusus penyisipan arc ketika:
        1. Beachline hanya memiliki satu arc dan ini adalah site kedua
        2. Site baru tepat berada di bawah site yang sudah ada
        
        Dalam kasus ini, intersection normal tidak bisa dihitung karena:
        - Belum ada breakpoint (untuk kasus pertama)
        - Parabola bertumpuk vertikal (untuk kasus kedua)
        
        Args:
            p: Titik fokus (site) untuk arc baru
            
        Returns:
            Arc: Arc yang baru disisipkan yang akan membagi arc yang ada
        """
        # Buat arc baru untuk site baru
        arc = Arc(point=p)
        
        # Mulai dari root
        current = self.root
        found = False
        
        # Traverse ke arc paling kanan di beachline
        # Ini penting karena dalam kasus khusus, arc baru harus
        # disisipkan setelah semua arc yang ada
        while not found:
            if current.next is not None:
                current = current.next
            else:
                found = True
                
        # Sisipkan arc baru setelah arc terakhir
        # Ini akan membuat urutan yang benar untuk kedua kasus khusus
        self.insert_successor(current, arc)
        return arc

    def insert_successor(self, p, s):
        """
        Menyisipkan arc sebagai successor dari arc yang diberikan.
        
        Args:
            p: Arc sebelumnya
            s: Arc yang akan disisipkan
        """
        # Update pointer untuk urutan beachline
        s.prev = p
        s.next = p.next
        p.next = s
        if s.next:
            s.next.prev = s
        
        # Sisipkan ke dalam Red-Black Tree
        if p.right is self.sentinel:
            self.add_as_right_child(s, p)
        else:
            r = p.right
            while r.left is not self.sentinel:
                r = r.left
            self.add_as_left_child(s, r)

    def delete_arc(self, arc):
        """
        Menghapus arc dari beachline.
        
        Args:
            arc: Arc yang akan dihapus
        """
        # Update pointer untuk urutan beachline
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