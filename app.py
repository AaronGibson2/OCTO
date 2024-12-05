# I M P O R T S   &   D E P E N D E N C I E S ----------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

# M A I N    M E N U   S E T   U P ---------------------------------
class PathfinderMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Florida Traffic Optimization")
        self.root.configure(bg='black')

        # Set default theme
        style = ttk.Style()
        style.theme_use('default')

        # Window setup
        window_width = 600
        window_height = 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = tk.Label(self.main_frame,
                              text="Florida SPF",
                              font=('Helvetica', 24, 'bold'),
                              bg='black',
                              fg='white')
        title_label.pack(pady=20)

        # City Selection & Set Up
        city_label = tk.Label(self.main_frame,
                             text="Select City:",
                             font=('Helvetica', 12),
                             bg='black',
                             fg='white')
        city_label.pack(pady=10)

        self.city_var = tk.StringVar()
        city_combo = ttk.Combobox(self.main_frame,
                                 textvariable=self.city_var,
                                 state='readonly',
                                 width=30)

        city_maps = self.get_available_maps()
        city_combo['values'] = city_maps
        city_combo.pack(pady=5)
        if city_maps:
            city_combo.set(city_maps[0])

        # Start Button
        self.start_button = tk.Button(
            self.main_frame,
            text="Start Pathfinder",
            command=self.start_pathfinder,
            font=('Helvetica', 12, 'bold'),
            bg='#FF8C00',
            fg='black',
            width=15,
            height=2,
            activebackground='#FF8C00',
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.start_button.pack(pady=30)

    # Gets list of maps from graph folerd
    def get_available_maps(self):
        maps = []
        data_dir = "graphml_files"
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith(".graphml"):
                    maps.append(file.replace(".graphml", ""))
        return maps

    # Launches main with desired city
    def start_pathfinder(self):
        city = self.city_var.get()

        if not city:
            messagebox.showerror("Error", "Please select a city map!")
            return

        print(f"Starting pathfinder in {city}")

        self.root.destroy()

        import main

        # Algorithm selectoin for main
        main.main('dijkstra', city_map=city)

# M A I N ----------------------------------------------------------
def main():
    root = tk.Tk()
    app = PathfinderMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
