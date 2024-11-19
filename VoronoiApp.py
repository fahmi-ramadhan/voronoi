# TUGAS PEMROGRAMAN GEOMETRI KOMPUTASIONAL
#
# Kelompok 12: - Fahmi Ramadhan (2206026473)
#              - Muhammad Nabiel Subhan (2206081553)
#              - Ken Balya (2206081811)
#
# Referensi: - https://www.slideshare.net/slideshow/fortunes-algorithm/238607094#33
#            - https://github.com/fewlinesofcode/FortunesAlgorithm


import tkinter as tk
from tkinter import filedialog, messagebox
from FortunesAlgo import FortunesAlgo
from Diagram import Diagram
from Rectangle import Rectangle
from Circle import Point
from Constant import eps
from scipy.spatial import KDTree

class MainWindow:
    """
    Jendela utama untuk visualisasi diagram Voronoi.
    
    Kelas ini mengimplementasikan aplikasi GUI yang memungkinkan pengguna untuk:
    - Membuat diagram Voronoi dengan mengklik titik-titik pada canvas
    - Memuat titik-titik dari file
    - Memvisualisasikan diagram Voronoi dengan sel dan vertex
    - Menemukan dan menampilkan lingkaran kosong terbesar di antara titik-titik
    
    Atribut:
        RADIUS (int): Radius titik yang digambar pada canvas (dalam piksel)
    """
    
    RADIUS = 3

    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi")
        
        # Membuat frame utama untuk menampung semua komponen
        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)
        
        # Membuat frame untuk tombol-tombol di bagian atas
        self.frmButtons = tk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X)
        
        # Menambahkan tombol untuk memuat titik dari file
        self.btnLoad = tk.Button(self.frmButtons, text="Load Points", command=self.load_points)
        self.btnLoad.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Menambahkan tombol untuk membersihkan canvas
        self.btnClear = tk.Button(self.frmButtons, text="Clear All", command=self.clear_canvas)
        self.btnClear.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Membuat canvas utama untuk menggambar
        self.canvas = tk.Canvas(self.frmMain, width=1440, height=720, bg="white")
        self.canvas.pack()
        
        # Menghubungkan klik kiri mouse dengan pembuatan titik
        self.canvas.bind('<Button-1>', self.on_click)
        
        # Inisialisasi struktur data
        self.points = []  # Daftar titik untuk akses berurutan
        self.diagram = Diagram()  # Struktur diagram Voronoi
        self.clipping_rect = Rectangle(0, 0, 1440, 720)  # Area pembatas diagram
        self.sweep = FortunesAlgo()  # Algoritma Fortune's sweep line untuk membuat diagram Voronoi

    def clear_canvas(self):
        """Membersihkan semua titik dan mereset canvas."""
        self.points = []
        self.canvas.delete(tk.ALL)

    def load_points(self):
        """
        Memuat titik-titik dari file teks.
        Format file yang diharapkan: setiap baris berisi koordinat x,y atau x y
        """
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not filename:  # Pengguna membatalkan
                return
                
            with open(filename, 'r') as file:
                # Membersihkan titik-titik yang ada
                self.points = []
                
                # Membaca titik-titik dari file
                for line in file:
                    try:
                        # Format yang diharapkan: "x,y" atau "x y"
                        coords = line.strip().replace(',', ' ').split()
                        if len(coords) == 2:
                            x, y = map(float, coords)
                            point = Point(x, y)
                            self.points.append(point)
                    except ValueError:
                        print(f"Melewati baris yang tidak valid: {line.strip()}")
                
            # Memperbarui diagram
            self.update_voronoi_diagram()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat titik-titik: {str(e)}")

    def on_click(self, event):
        """
        Menangani event klik mouse pada canvas.
        Menambahkan titik baru dan memperbarui diagram Voronoi.
        
        Args:
            event: Event klik mouse
        """
        point = Point(event.x, event.y)
        self.points.append(point)
        self.update_voronoi_diagram()

    def update_voronoi_diagram(self):
        """
        Memperbarui diagram Voronoi berdasarkan titik-titik yang ada.
        Mencetak informasi sel dan vertex ke konsol.
        """
        if self.points:  # Hanya memperbarui jika ada titik
            self.diagram.clear()
            sites = set(self.points)
            self.sweep.compute(sites, self.diagram, self.clipping_rect)
            self.draw_voronoi()

    def draw_voronoi(self):
        """
        Menggambar diagram Voronoi pada canvas.
        Termasuk:
        - Sel-sel Voronoi (garis biru)
        - Titik-titik input (lingkaran hitam)
        - Vertex-vertex diagram (titik merah)
        - Lingkaran kosong terbesar (garis oranye)
        """
        self.canvas.delete(tk.ALL)
        
        # Menggambar sel-sel Voronoi
        for cell in self.diagram.cells:
            if cell.outer_component:
                he = cell.outer_component
                points = []
                while True:
                    if he.origin:
                        points.append((he.origin.x, he.origin.y))
                    he = he.next
                    if he == cell.outer_component or he is None:
                        break
                if points:
                    self.canvas.create_polygon(points, outline="blue", fill="", tags="voronoi")
        
        # Menggambar titik-titik input
        for point in self.points:
            self.canvas.create_oval(point.x - self.RADIUS, point.y - self.RADIUS, 
                                  point.x + self.RADIUS, point.y + self.RADIUS, fill="black")
        
        # Mempersiapkan KD-Tree untuk pencarian titik terdekat
        site_coords = [(point.x, point.y) for point in self.points]
        tree = KDTree(site_coords)

        # Menggambar vertex-vertex
        for vertex in self.diagram.vertices:
            # print(vertex.x, vertex.y)
            self.canvas.create_oval(vertex.x - 1.5, vertex.y - 1.5, 
                                  vertex.x + 1.5, vertex.y + 1.5, fill="red", outline="red", tags="vertex")

        # Mencari dan menggambar lingkaran kosong terbesar
        centers = []
        radiuses = []
        max_radius = -1
        for vertex in self.diagram.vertices:
            vx, vy = vertex.x, vertex.y
            
            # Mencari 5 titik terdekat untuk setiap vertex
            distances, indices = tree.query((vx, vy), k=5)  
            
            radius = distances[0]
            close_sites = [(site_coords[i][0], site_coords[i][1]) for i, d in zip(indices, distances) if abs(d - radius) < eps]

            if len(close_sites) >= 3:
                centers.append((vx, vy))
                radiuses.append(radius)
                max_radius = max(radius, max_radius)

        # Menggambar lingkaran kosong terbesar
        for i in range(len(centers)):
            radius = radiuses[i]
            if radius == max_radius:
                vx = centers[i][0]
                vy = centers[i][1]
                self.canvas.create_oval(vx - radius, vy - radius, vx + radius, vy + radius,
                                     outline="orange", tags="largest_empty_circle")
            
def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
