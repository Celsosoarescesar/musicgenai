import reapy
import tkinter as tk

# REDEFINE THESE NOTES AT WILL (Live Coding)
PITCHES   = [64, 65, 64] # E4, F4, E4
DURATIONS = [250, 250, 500] # Sixteenth, Sixteenth, Eighth (ms at 60 BPM)

def setup_reaper():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    track_name = "Terry Riley In C"
    
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

class InCPerformance:
    def __init__(self):
        self.project = setup_reaper()
        self.is_playing = False
        
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Terry Riley: In C (Live Performance)")
        self.root.geometry("300x150")
        
        tk.Label(self.root, text="Tema: E4, F4, E4", font=("Arial", 12)).pack(pady=10)
        
        self.btn_toggle = tk.Button(self.root, text="Start Performance", 
                                    command=self.toggle_performance, 
                                    bg="green", fg="white", font=("Arial", 10, "bold"))
        self.btn_toggle.pack(pady=10)
        
        tk.Label(self.root, text="Edit reapy_terry_riley_in_c.py\nto change notes live!", fg="gray").pack()

    def toggle_performance(self):
        if not self.is_playing:
            self.is_playing = True
            self.btn_toggle.config(text="Stop Performance", bg="red")
            print("Performance started...")
            self.loop_music(0) # Start from first note
        else:
            self.is_playing = False
            self.btn_toggle.config(text="Start Performance", bg="green")
            print("Performance stopped.")
            # Silence all notes
            reapy.RPR.StuffMIDIMessage(0, 0xb0, 123, 0) # All notes off

    def loop_music(self, note_idx):
        if not self.is_playing: return

        # Play current note
        pitch = PITCHES[note_idx]
        duration = DURATIONS[note_idx]
        
        # Note On
        reapy.RPR.StuffMIDIMessage(0, 0x90, pitch, 100)
        
        # Schedule Note Off
        self.root.after(duration - 10, lambda p=pitch: reapy.RPR.StuffMIDIMessage(0, 0x80, p, 0))
        
        # Schedule NEXT Note in the theme
        next_idx = (note_idx + 1) % len(PITCHES)
        self.root.after(duration, lambda: self.loop_music(next_idx))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = InCPerformance()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
