import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import sys

# --- Constants ---
TILE_SIZE = 150  # The width and height of your tile images in pixels
GRID_DIM = 3     # The grid is 3x3

class SolutionViewer:
    """
    A GUI to visualize the solution path for the Temple Trap game.
    """
    def __init__(self, master, solution_path, initial_state,final_path_cost):
        """
        Initializes the viewer window.
        
        Args:
            master (tk.Tk): The root tkinter window.
            solution_path (list): A list of state tuples.
        """
        if not solution_path:
            print("Error: Solution path cannot be empty.")
            sys.exit()

        self.master = master
        self.solution_path = solution_path
        self.current_state_index = 0
        self.path_cost_var = tk.StringVar()
        self.path_cost_var.set(f"PATH COST: {self.current_state_index}")
        self.is_playing = False
        self.initial_state=initial_state.strip().split()
        self.final_path_cost = final_path_cost
        
        # --- Window Configuration ---
        self.master.title("Temple Trap")
        self.master.configure(bg='white')
        

        # --- Load Images ---
        self.image_cache = self._load_images()
        if not self.image_cache:
            # _load_images will print an error and exit if files are missing
            return 
            
        # --- Create Widgets ---
        self._create_widgets()
        
        # --- Initial Display ---
        self.update_display()
        self.master.resizable(False, False)
        
        # Ensure the play loop stops if the window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.end_program)
        self.steps = 0
        


    def _load_images(self):
        """
        Pre-loads all required PNG images.
        Stores both the raw Pillow Images (for manipulation) and the
        display-ready ImageTk PhotoImages.
        """
        # This cache will hold the raw Pillow Image objects
        self.pillow_images = {}
        # This cache will hold the Tkinter-ready PhotoImage objects
        image_cache = {}
        
        # tile_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'empty', 'player']
        try:
            for config in self.initial_state[:-1]:
                filepath = f"./Tiles/{config[1]}.png"
                # Open the image with Pillow
                image = Image.open(filepath).convert("RGBA")
                # Resize to ensure consistency
                image = image.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)
                image = image.rotate(-1*90*int(config[2]))
                
                # Store the raw Pillow image
                self.pillow_images[config[1]] = image
                # Store the Tkinter-ready image
                image_cache[config[1]] = ImageTk.PhotoImage(image)
                
            static_images = ['empty', 'player', 'player_win'] # <-- CHANGE 1: ADDED 'player_won'
            for name in static_images:
                filepath = f"./Tiles/{name}.png"
                image = Image.open(filepath).convert("RGBA")
                image = image.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)
                self.pillow_images[name] = image
                image_cache[name] = ImageTk.PhotoImage(image) # Store non-rotated version

            return image_cache
        except FileNotFoundError as e:
            print(f"Error: Missing image file! -> {e}")
            self.master.destroy()
            sys.exit()


    def _create_widgets(self):
        """
        Creates and lays out all the GUI widgets.
        """
        # --- Title ---
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        title = tk.Label(
            self.master, 
            text="Temple Trap", 
            font=title_font, 
            bg='#007FFF', 
            fg='white', 
            pady=10
        )
        # Explicitly pack the title at the TOP
        title.pack(side='top', fill='x')   
        

        self.path_cost_button = tk.Button(self.master, text=f"PATH COST: {self.current_state_index}/{self.final_path_cost}", font=("Arial", 14), bg="lightgray")
        self.path_cost_button.pack(pady=(5, 15))  # Adjust vertical spacing as needed

        # --- Control Buttons ---
        # NOTE: We create and PACK the bottom frame BEFORE the middle content
        button_frame = tk.Frame(self.master, bg='white')
        # Explicitly pack the buttons at the BOTTOM
        button_frame.pack(side='bottom', fill='x', pady=10)
        
        button_font = font.Font(family='Helvetica', size=14)
        
        self.prev_button = tk.Button(button_frame, text="Previous", font=button_font, command=self.show_previous)
        self.next_button = tk.Button(button_frame, text="Next", font=button_font, command=self.show_next)
        self.play_button = tk.Button(button_frame, text="Play", font=button_font, command=self.toggle_play)
        self.end_button = tk.Button(button_frame, text="End", font=button_font, command=self.end_program)
        
        # Use pack to distribute buttons evenly within their frame
        self.prev_button.pack(side='left', expand=True, fill='x')
        self.next_button.pack(side='left', expand=True, fill='x')
        self.play_button.pack(side='left', expand=True, fill='x')
        self.end_button.pack(side='left', expand=True, fill='x')

        # --- Grid Frame ---
        # NOW, we create and pack the main grid. It will fill the space
        # between the title (top) and the button_frame (bottom).
        self.grid_frame = tk.Frame(
            self.master, 
            width=GRID_DIM * TILE_SIZE, 
            height=GRID_DIM * TILE_SIZE
        )
        # The 'expand=True' is crucial. It tells the frame to fill available space.
        self.grid_frame.pack(side='top', expand=True, pady=20)
        
        # Create labels for the grid tiles
        self.tile_labels = []
        for i in range(GRID_DIM * GRID_DIM):
            row, col = divmod(i, GRID_DIM)
            label = tk.Label(self.grid_frame, borderwidth=0)
            label.grid(row=row, column=col)
            self.tile_labels.append(label)
            
 


    def update_display(self):
        """
        Updates the grid tiles. The player is drawn by creating a composite
        image of the player on top of the underlying tile.
        """
        game_won=False
        current_state = self.solution_path[self.current_state_index]
        board_config = current_state[:-1]
        if current_state[-1] == -1:
            game_won = True
            player_pos_index=0
        else:
            player_pos_index = current_state[-1]

        # 1. First, draw the plain board without the player
        for i, tile_name in enumerate(board_config):
            base_image = self.image_cache.get(tile_name)
            if base_image:
                self.tile_labels[i].config(image=base_image)

        # 2. Identify the tile the player is on
        tile_under_player_name = board_config[player_pos_index]
        target_label = self.tile_labels[player_pos_index]

        # 3. Get the raw Pillow images for the base tile and the player
        base_tile_img = self.pillow_images[tile_under_player_name].copy()
        if game_won:
            player_img = self.pillow_images['player_win']
        else:
            player_img = self.pillow_images['player']

        # 4. Composite the player image onto the tile image.
        # The third argument (player_img) acts as a mask, using its own alpha channel.
        base_tile_img.paste(player_img, (0, 0), player_img)

        # 5. Convert the new composite image to a PhotoImage for display
        composite_photo = ImageTk.PhotoImage(base_tile_img)

        # 6. IMPORTANT: Keep a reference to the new image to prevent garbage collection
        target_label.composite_image = composite_photo
        
        # 7. Update the specific tile label with the new composite image
        target_label.config(image=composite_photo)
        
        # 8. Update button states (this part is unchanged)
        self.prev_button.config(state='normal' if self.current_state_index > 0 else 'disabled')
        self.next_button.config(state='normal' if self.current_state_index < len(self.solution_path) - 1 else 'disabled')
        if self.current_state_index == len(self.solution_path) - 1:
            if self.is_playing:
                self.toggle_play()
    def show_next(self):
        """Go to the next state in the solution path."""
        if self.current_state_index < len(self.solution_path) - 1:
            self.current_state_index += 1
            self.path_cost_button.config(text=f"PATH COST: {self.current_state_index}/{self.final_path_cost}")
            self.update_display()

    def show_previous(self):
        """Go to the previous state in the solution path."""
        if self.current_state_index > 0:
            self.current_state_index -= 1
            self.path_cost_button.config(text=f"PATH COST: {self.current_state_index}/{self.final_path_cost}")
            self.update_display()
            
    def toggle_play(self):
        """Starts or stops the automatic playback of states."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.config(text="Pause")
            self._play_step()
        else:
            self.play_button.config(text="Play")
            
    def _play_step(self):
        """Performs one step of the playback and schedules the next."""
        if self.is_playing:
            self.show_next()
            # If not at the end, schedule the next step after 1 second (1000 ms)
            if self.current_state_index < len(self.solution_path) - 1:
                self.master.after(1000, self._play_step)
            else:
                self.is_playing = False
                self.play_button.config(text="Play")

    def end_program(self):
        """Stops any running loops and closes the window."""
        self.is_playing = False # Stop any pending 'after' calls
        self.master.destroy()


# --- Main execution block ---
