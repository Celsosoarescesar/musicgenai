import reapy
import tkinter as tk

def setup_reaper():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    track_name = "iPiano"
    
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

class IPianoApp:
    def __init__(self):
        self.project = setup_reaper()
        self.notes_active = set() # Track active MIDI pitches to prevent key-repeat
        
        # Mapping PC keys to MIDI notes (C4 = 60)
        self.key_map = {
            'z': 60,  # C
            's': 61,  # C#
            'x': 62,  # D
            'd': 63,  # D#
            'c': 64,  # E
            'v': 65,  # F
            'g': 66,  # F#
            'b': 67,  # G
            'h': 68,  # G#
            'n': 69,  # A
            'j': 70,  # A#
            'm': 71,  # B
            ',': 72   # C5
        }
        
        # Store canvas IDs for piano keys to highlight them
        self.key_rects = {}
        
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("iPiano Simple")
        self.root.geometry("450x250")
        
        self.canvas = tk.Canvas(self.root, width=450, height=200, bg="gray")
        self.canvas.pack(pady=10)
        
        # Draw Piano Keyboard
        white_keys = ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',']
        black_keys = {
            's': 0.7, # relative pos between first and second white key
            'd': 1.7,
            'g': 3.7,
            'h': 4.7,
            'j': 5.7
        }
        
        w_width = 50
        w_height = 180
        
        # Draw White Keys
        for i, char in enumerate(white_keys):
            x1 = i * w_width + 25
            rect = self.canvas.create_rectangle(x1, 10, x1 + w_width, 10 + w_height, fill="white", outline="black")
            self.key_rects[char] = rect
            self.canvas.create_text(x1 + 25, 175, text=char.upper(), fill="gray")

        # Draw Black Keys (overlay)
        b_width = 30
        b_height = 110
        for char, pos in black_keys.items():
            x1 = pos * w_width + 25 + (w_width - b_width/2)
            rect = self.canvas.create_rectangle(x1, 10, x1 + b_width, 10 + b_height, fill="black", outline="black")
            self.key_rects[char] = rect
            self.canvas.create_text(x1 + 15, 95, text=char.upper(), fill="white")

        # Bind window events
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        tk.Label(self.root, text="Play using keys: Z S X D C V G B H N J M ,").pack()

    def on_key_press(self, event):
        char = event.char.lower()
        if char in self.key_map and char not in self.notes_active:
            pitch = self.key_map[char]
            self.notes_active.add(char)
            
            # Highlight GUI
            fill = "cyan" if self.canvas.itemcget(self.key_rects[char], "fill") == "white" else "blue"
            self.canvas.itemconfig(self.key_rects[char], fill=fill)
            
            # Play in REAPER
            reapy.RPR.StuffMIDIMessage(0, 0x90, pitch, 100)

    def on_key_release(self, event):
        char = event.char.lower()
        if char in self.key_map and char in self.notes_active:
            pitch = self.key_map[char]
            self.notes_active.remove(char)
            
            # Restore GUI color
            original_fill = "white" if char in ['z', 'x', 'c', 'v', 'b', 'n', 'm', ','] else "black"
            self.canvas.itemconfig(self.key_rects[char], fill=original_fill)
            
            # Stop in REAPER
            reapy.RPR.StuffMIDIMessage(0, 0x80, pitch, 0)

    def run(self):
        print("iPiano Active. Play your computer keyboard!")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = IPianoApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
