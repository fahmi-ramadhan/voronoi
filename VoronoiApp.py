import tkinter as tk
from tkinter import filedialog, messagebox
from FortuneSweep import FortuneSweep
from Diagram import Diagram
from Rectangle import Rectangle
from Circle import Point

class MainWindow:
    # radius of drawn points on canvas
    RADIUS = 3

    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi")
        
        # Create main frame
        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)
        
        # Create button frame
        self.frmButtons = tk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X)
        
        # Add load button
        self.btnLoad = tk.Button(self.frmButtons, text="Load Points", command=self.load_points)
        self.btnLoad.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add clear button
        self.btnClear = tk.Button(self.frmButtons, text="Clear All", command=self.clear_canvas)
        self.btnClear.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create canvas
        self.canvas = tk.Canvas(self.frmMain, width=500, height=500, bg="white")
        self.canvas.pack()
        
        self.canvas.bind('<Button-1>', self.on_click)
        
        self.points = []
        self.points_set = set()
        self.diagram = Diagram()
        self.clipping_rect = Rectangle(0, 0, 510, 510)
        self.sweep = FortuneSweep()

    def clear_canvas(self):
        """Clear all points and reset the canvas."""
        self.points = []
        self.points_set = set()
        self.canvas.delete(tk.ALL)

    def load_points(self):
        """Load points from a text file."""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not filename:  # User canceled
                return
                
            with open(filename, 'r') as file:
                # Clear existing points
                self.points = []
                self.points_set = set()
                
                # Read points from file
                for line in file:
                    try:
                        # Expecting format: "x,y" or "x y"
                        coords = line.strip().replace(',', ' ').split()
                        if len(coords) == 2:
                            x, y = map(float, coords)
                            point = (int(x), int(y))
                            if point not in self.points_set:
                                self.points.append(point)
                                self.points_set.add(point)
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
                
            # Update the diagram
            self.update_voronoi_diagram()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load points: {str(e)}")

    def on_click(self, event):
        point = (event.x, event.y)
        if point not in self.points_set:
            self.points.append(point)
            self.points_set.add(point)
            self.update_voronoi_diagram()

    def update_voronoi_diagram(self):
        if self.points:  # Only update if there are points
            self.diagram.clear()
            sites = {Point(x, y) for x, y in self.points}
            self.sweep.compute(sites, self.diagram, self.clipping_rect)
            self.draw_voronoi()

    def draw_voronoi(self):
        self.canvas.delete(tk.ALL)
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
        for x, y in self.points:
            self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, 
                                    x + self.RADIUS, y + self.RADIUS, fill="black")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()