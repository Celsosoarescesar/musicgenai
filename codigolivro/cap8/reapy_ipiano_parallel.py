import reapy
import tkinter as tk

def setup_reaper():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    track_name = "iPiano Parallel"
    
    # Find or create track
    target_track = None
    for track in project.tracks:
        if track.name == track_name:
            target_track = track
            break
    
    if not target_track:
        target_track = project.add_track(name=track_name)
        target_track.add_fx("ReaSynth")
        
    # Arm and Monitor
    target_track.is_armed = True
    target_track.set_info_value("I_RECMON", 1) # Monitoring ON
    return project

class IPianoParallelApp:
    def __init__(self):
        self.project = setup_reaper()
        self.keys_pressed = [] # Track active keys to prevent repetition

        # Parallel lists representing the instrument configuration
        self.virtual_keys = ['z', 's', 'x', 'd', 'c', 'v']
        self.pitches      = [60,  61,  62,  63,  64,  65] # C4, CS4, D4, DS4, E4, F4
        self.rect_ids     = [None] * len(self.virtual_keys) # To hold tkinter IDs
        
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("iPiano Parallel")
        self.root.geometry("450x250")
        
        self.canvas = tk.Canvas(self.root, width=450, height=200, bg="#aaaaaa")
        self.canvas.pack(pady=10)

        # Mapping of coordinates based on the book's icons (roughly)
        # 0, 45, 76, 138, 150, 223
        x_coords = [25, 65, 95, 145, 165, 235]
        
        # Draw the piano keys
        for i in range(len(self.virtual_keys)):
            char = self.virtual_keys[i]
            is_black = char in ['s', 'd'] # Simplified check for this range
            
            width = 30 if is_black else 50
            height = 110 if is_black else 180
            fill_color = "black" if is_black else "white"
            text_color = "white" if is_black else "gray"
            
            x1 = x_coords[i]
            y1 = 10
            
            rect = self.canvas.create_rectangle(x1, y1, x1 + width, y1 + height, fill=fill_color, outline="black")
            self.rect_ids[i] = rect
            
            # Add label
            label_y = y1 + height - 15
            self.canvas.create_text(x1 + width/2, label_y, text=char.upper(), fill=text_color)

        # Bind window events
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        tk.Label(self.root, text="Parallel List Instrument: Z S X D C V").pack()

    def on_key_press(self, event):
        key = event.char.lower()
        
        # Iterate through parallel lists
        for i in range(len(self.virtual_keys)):
            if key == self.virtual_keys[i] and key not in self.keys_pressed:
                pitch = self.pitches[i]
                self.keys_pressed.append(key)
                
                # Highlight in GUI
                is_black = key in ['s', 'd']
                highlight = "blue" if is_black else "cyan"
                self.canvas.itemconfig(self.rect_ids[i], fill=highlight)
                
                # Play in REAPER
                reapy.RPR.StuffMIDIMessage(0, 0x90, pitch, 100)

    def on_key_release(self, event):
        key = event.char.lower()
        
        # Iterate through parallel lists
        for i in range(len(self.virtual_keys)):
            if key == self.virtual_keys[i]:
                pitch = self.pitches[i]
                if key in self.keys_pressed:
                    self.keys_pressed.remove(key)
                
                # Restore original color
                is_black = key in ['s', 'd']
                original_color = "black" if is_black else "white"
                self.canvas.itemconfig(self.rect_ids[i], fill=original_color)
                
                # Stop in REAPER
                reapy.RPR.StuffMIDIMessage(0, 0x80, pitch, 0)

    def run(self):
        print("iPiano Parallel Active. Play Z S X D C V!")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = IPianoParallelApp()
        app.run()
    except Exception as e:
        # - [x] Planning the port <!-- id: 0 -->
        # - [/] Implement `reapy_random_circles_timed.py` in `cap8` <!-- id: 1 -->
        # - [/] Manual verification <!-- id: 2 -->
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
