import reapy
import tkinter as tk
import random

def setup_reaper():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    track_name = "Timed Circles"
    
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

class RandomCirclesTimedApp:
    def __init__(self):
        self.project = setup_reaper()
        self.delay = 500 # ms
        self.is_running = True
        
        self.setup_gui()
        # Start the generation loop
        self.root.after(self.delay, self.draw_cycle)

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Random Timed Circles with Sound")
        
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        
        # Control window (built into same root for simplicity)
        controls = tk.Frame(self.root)
        controls.pack(pady=10)
        
        tk.Label(controls, text="Generation Delay (ms):").pack(side="left")
        self.slider = tk.Scale(controls, from_=10, to_=1000, orient="horizontal", 
                               command=self.update_delay, length=200)
        self.slider.set(self.delay)
        self.slider.pack(side="left", padx=10)

    def update_delay(self, val):
        self.delay = int(val)
        self.root.title(f"Random Timed Circles (Delay: {self.delay}ms)")

    def draw_cycle(self):
        if not self.is_running: return

        # 1. Random parameters
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        radius = random.randint(5, 40)
        
        red = random.randint(100, 255)
        blue = random.randint(0, 100)
        color_hex = '#{:02x}00{:02x}'.format(red, blue)
        
        # 2. Draw on canvas
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color_hex, outline="")

        # 3. Sonify
        # map 255-red+blue to pitch range C4 (60) to C6 (84)
        input_val = 255 - red + blue
        pitch_raw = 60 + (input_val / 255.0) * (84 - 60)
        pitch = quantize_to_major(int(pitch_raw))
        
        # map radius (5-40) to velocity (20-127)
        velocity = int(20 + ((radius - 5) / 35.0) * (127 - 20))
        
        # Play in REAPER
        reapy.RPR.StuffMIDIMessage(0, 0x90, pitch, velocity)
        # Schedule Note Off after 5 seconds
        self.root.after(5000, lambda p=pitch: reapy.RPR.StuffMIDIMessage(0, 0x80, p, 0))

        # 4. Schedule next cycle
        self.root.after(self.delay, self.draw_cycle)

    def run(self):
        print("Generative Artist active. Circles and sound started.")
        self.root.mainloop()
        self.is_running = False

if __name__ == "__main__":
    try:
        app = RandomCirclesTimedApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
