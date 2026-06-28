import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from search import search
from solution_viewer import SolutionViewer

import os
base_dir = os.path.dirname(os.path.abspath(__file__))

class TempleTrapGUI:
    """
    A class to create and manage the Temple Trap Game configuration GUI.
    """
    def __init__(self, master):
        """
        Initializes the GUI window and its widgets.
        """
        self.master = master
        self.user_input = None  # This will store the final input string

        # --- Window Configuration ---
        self.master.title("Temple Trap Game")
        self.master.configure(bg='white')
        
        # Set window size and center it on the screen
        window_width = 550
        window_height = 800
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # --- Title ---
        title_font = font.Font(family='Helvetica', size=28, weight='bold')
        title_label = tk.Label(
            self.master, 
            text="Temple Trap Game", 
            font=title_font, 
            bg='#007FFF',  # A nice bright blue
            fg='white', 
            padx=20, 
            pady=10
        )
        title_label.pack(pady=30)

        # --- 3x3 Tile Grid ---
        grid_frame = tk.Frame(self.master, bg='white')
        grid_frame.pack(pady=10)

        tile_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        tile_images = []
        for name in tile_names:
            filepath = os.path.join(base_dir, "Tiles", f"{name}.png")
            img = Image.open(filepath).resize((100, 100))
            tile_images.append(ImageTk.PhotoImage(img))

        tile_label_font = font.Font(family='Helvetica', size=16)
        for i in range(3):
            for j in range(3):
                # Container for each tile (black square + 'A' label)
                index = i * 3 + j
                if index >= 8:
                    break
                tile_container = tk.Frame(grid_frame, bg='white')
                tile_container.grid(row=i, column=j, padx=25, pady=15)

                # Black square represented by a Canvas
                canvas = tk.Label(tile_container, image=tile_images[index])
                canvas.image = tile_images[index]  # Prevent garbage collection
                canvas.pack()

                # Label 'A' below the square
                label = tk.Label(tile_container, text=f"{tile_names[index]}", font=tile_label_font, bg='white')
                label.pack(pady=5)
        
        # --- Input Section ---
        input_frame = tk.Frame(self.master, bg='white')
        input_frame.pack(pady=20, fill='x', padx=20)

        config_label = tk.Label(input_frame, text="Enter Initial Configuration", bg='white', font=('Helvetica', 14))
        config_label.pack()

        # Entry widget for user input
        self.config_var = tk.StringVar()
        entry_box = tk.Entry(
            input_frame, 
            textvariable=self.config_var, 
            width=50, 
            bg='#E0E0E0',  # Light grey background
            relief='solid', 
            borderwidth=1, 
            font=('Courier', 11)
        )
        entry_box.pack(pady=10, ipady=5)
        entry_box.focus_set()  # Automatically focus the input box

        # Bind the <Return> (Enter key) event to the on_enter method
        entry_box.bind('<Return>', self.on_enter)

        # Description labels
        desc_font = ('Helvetica', 10)
        tk.Label(input_frame, text="Example Configuration: 0D1 1B2 2C1 3G0 4F2 5A3 6H3 7E3 0", bg='white', font=desc_font).pack()
        tk.Label(input_frame, text="(Position TileType Rotation)", bg='white', font=desc_font).pack()
        tk.Label(input_frame, text="Last entry is Player Position", bg='white', font=desc_font).pack()

    def on_enter(self, event):
        """
        This method is called when the user presses the Enter key.
        It saves the input and closes the window.
        """
        self.user_input = self.config_var.get()
        print(f"Configuration captured: '{self.user_input}'")
        self.master.destroy() # Closes the Tkinter window

def get_initial_configuration():
    """
    Function to launch the GUI and return the user's input.
    This function will pause execution of the script until the GUI window is closed.
    """
    root = tk.Tk()
    app = TempleTrapGUI(root)
    root.mainloop()  # This line blocks until the window is destroyed
    return app.user_input

# --- Main execution block ---
if __name__ == "__main__":
    print("Opening GUI to get initial configuration...")
    
    # This function call will display the GUI and wait for user input
    initial_config = get_initial_configuration()

    # The code below will only run after the GUI window is closed
    if initial_config is not None:
        print(f"'{initial_config}'")
    else:
        print("\nGUI was closed without providing a configuration.")

    
    # --- EXAMPLE USAGE ---
    # This is a sample list of state tuples.
    # Replace this with the actual list of states you generate.
    solution, path_cost = search(initial_config)

    # Create the main window and run the app
    root = tk.Tk()
    app = SolutionViewer(root, solution, initial_config, path_cost)
    root.mainloop()
    
    print("Viewer closed.")