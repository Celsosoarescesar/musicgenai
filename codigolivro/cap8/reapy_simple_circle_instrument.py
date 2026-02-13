import reapy
import tkinter as tk
import math

def setup_reaper():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    track_name = "Circle Instrument"
    
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

def quantize_to_major(pitch):
    """Quantizes MIDI pitch to C Major scale."""
    scale = [0, 2, 4, 5, 7, 9, 11]
    octave = pitch // 12
    note = pitch % 12
    closest = min(scale, key=lambda x: abs(x - note))
    return (octave * 12) + closest

class CircleInstrument:
    def __init__(self):
        self.project = setup_reaper()
        self.begin_x = 0
        self.begin_y = 0
        
        # Pitch range (MIDI)
        self.min_pitch = 24 # C1
        self.max_pitch = 108 # C8
        
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Circle Instrument")
        
        self.width = 600
        self.height = 400
        self.max_diameter = math.sqrt(self.width**2 + self.height**2)
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#33ccff")
        self.canvas.pack()
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<space>", self.clear_canvas)
        
        tk.Label(self.root, text="Click and Drag to Draw Circles | Space to Clear").pack()

    def on_press(self, event):
        self.begin_x = event.x
        self.begin_y = event.y

    def on_release(self, event):
        end_x = event.x
        end_y = event.y
        
        # Calculate parameters
        diameter = math.sqrt((self.begin_x - end_x)**2 + (self.begin_y - end_y)**2)
        radius = diameter / 2
        center_x = (self.begin_x + end_x) / 2
        center_y = (self.begin_y + end_y) / 2
        
        if diameter < 2: return # Too small
        
        # Draw on canvas
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline="yellow", width=3
        )
        
        # Calculate Pitch
        # Original: map diameter to pitch, then invert
        pitch_val = (diameter / self.max_diameter) * (self.max_pitch - self.min_pitch)
        pitch = self.max_pitch - pitch_val
        
        # Quantize and clamp
        midi_pitch = quantize_to_major(int(pitch))
        midi_pitch = max(self.min_pitch, min(self.max_pitch, midi_pitch))
        
        # Play in REAPER (StuffMIDIMessage mode 0 = Virtual MIDI Keyboard)
        # 0x90 = Note On. Note: We use a fixed duration approach by sending Off later
        # However, the original says 'Note(pitch, 0, 5000)' which holds for 5s.
        # We'll send Note On now.
        reapy.RPR.StuffMIDIMessage(0, 0x90, midi_pitch, 100)
        
        # Schedule Note Off after 5 seconds
        self.root.after(5000, lambda p=midi_pitch: reapy.RPR.StuffMIDIMessage(0, 0x80, p, 0))

    def clear_canvas(self, event):
        self.canvas.delete("all")
        # All Notes Off (CC 123)
        reapy.RPR.StuffMIDIMessage(0, 0xB0, 123, 0)
        print("Canvas cleared and sound stopped.")

    def run(self):
        print("Circle Instrument active. Draw on the canvas!")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = CircleInstrument()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
