# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import tkinter as tk
from tkinter import ttk

# S T A T   W I N D O W   S E T   U P ------------------------------
class StatWindow:
    def __init__(self, root, elapsed_time_dijkstra, elapsed_time_aStar,
                 num_nodes_visited_dijkstra, num_nodes_visited_aStar,
                 distance_dijkstra, distance_aStar):
        
        self.root = root
        self.root.title("Algorithm Stats")
        self.root.configure(bg='black')

        # Set default theme
        style = ttk.Style()
        style.theme_use('default')

        # Configure style for separator
        style.configure("TSeparator", background="white")

        # Window setup
        window_width = 400
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        tk.Label(self.main_frame, text="Algorithm Comparison",
                fg='white', bg='black', font=('Arial', 14, 'bold')).pack(pady=10)

        # Labels for Dijkstra's Algorithm
        tk.Label(self.main_frame, text="Dijkstra's Algorithm",
                fg='#FF8C00', bg='black', font=('Arial', 12, 'bold')).pack(pady=5)

        tk.Label(self.main_frame,
                text=f"Execution Time: {elapsed_time_dijkstra:.6f} seconds",
                fg='white', bg='black', font=('Arial', 10)).pack()

        tk.Label(self.main_frame,
                text=f"Nodes Visited: {num_nodes_visited_dijkstra}",
                fg='white', bg='black', font=('Arial', 10)).pack()

        tk.Label(self.main_frame,
                text=f"Total Distance: {distance_dijkstra:.2f} meters",
                fg='white', bg='black', font=('Arial', 10)).pack()

        # Little line
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Labels for A* Algorithm
        tk.Label(self.main_frame, text="A* Algorithm",
                fg='#0096FF', bg='black', font=('Arial', 12, 'bold')).pack(pady=5)

        tk.Label(self.main_frame,
                text=f"Execution Time: {elapsed_time_aStar:.6f} seconds",
                fg='white', bg='black', font=('Arial', 10)).pack()

        tk.Label(self.main_frame,
                text=f"Nodes Visited: {num_nodes_visited_aStar}",
                fg='white', bg='black', font=('Arial', 10)).pack()

        tk.Label(self.main_frame,
                text=f"Total Distance: {distance_aStar:.2f} meters",
                fg='white', bg='black', font=('Arial', 10)).pack()

        # Performance Comparison
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Calculate performance differences
        time_diff = (elapsed_time_dijkstra - elapsed_time_aStar) / elapsed_time_dijkstra * 100
        node_diff = (num_nodes_visited_dijkstra - num_nodes_visited_aStar) / num_nodes_visited_dijkstra * 100

        # Show which algorithm performed better
        time_better = "A*" if elapsed_time_aStar < elapsed_time_dijkstra else "Dijkstra's"
        nodes_better = "A*" if num_nodes_visited_aStar < num_nodes_visited_dijkstra else "Dijkstra's"

        tk.Label(self.main_frame, text="Performance Analysis",
                fg='white', bg='black', font=('Arial', 12, 'bold')).pack(pady=5)

        tk.Label(self.main_frame,
                text=f"{time_better} was {abs(time_diff):.1f}% faster",
                fg='white', bg='black', font=('Arial', 10)).pack()

        tk.Label(self.main_frame,
                text=f"{nodes_better} visited {abs(node_diff):.1f}% fewer nodes",
                fg='white', bg='black', font=('Arial', 10)).pack()

# Creates stat window
def create_stat_window(elapsed_time_dijkstra, elapsed_time_aStar,
                      num_nodes_visited_dijkstra, num_nodes_visited_aStar,
                      distance_dijkstra, distance_aStar):
    root = tk.Tk()
    StatWindow(root, elapsed_time_dijkstra, elapsed_time_aStar,
                  num_nodes_visited_dijkstra, num_nodes_visited_aStar,
                  distance_dijkstra, distance_aStar)
    return root
