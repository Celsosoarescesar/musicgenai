import reapy
import tkinter as tk
import os
import wave
import math
import struct

def create_test_audio(path):
    """Creates a 1-second sine wave (440Hz) if missing."""
    if os.path.exists(path):
        return
    print(f"Generating test audio: {path}")
    sample_rate = 44100.0
    duration = 1.0  # seconds
    frequency = 440.0
    num_samples = int(sample_rate * duration)
    
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(int(sample_rate))
        for i in range(num_samples):
            val = int(32767.0 * math.sin(2.0 * math.pi * frequency * (i / sample_rate)))
            f.writeframesraw(struct.pack('<h', val))

class ContinuousPitchInstrument:
    def __init__(self):
        self.project = reapy.Project()
        self.track_name = "Continuous Audio Instrument"
        self.item = None
        self.track = None
        self.setup_reaper()
        self.setup_gui()

    def setup_reaper(self):
        # 1. Audio setup
        audio_path = os.path.join(os.path.dirname(__file__), "test_loop.wav")
        create_test_audio(audio_path)

        # 2. Track setup
        self.track = None
        for t in self.project.tracks:
            if t.name == self.track_name:
                self.track = t
                break
        
        if not self.track:
            self.track = self.project.add_track(name=self.track_name)
        
        # 3. Add item and loop it
        # Clear existing items on track to avoid overlap
        for item in self.track.items:
            item.delete()
            
        # Move cursor to 0 and select track for accurate insertion
        reapy.RPR.SetEditCurPos(0, False, False)
        # Select ONLY this track
        reapy.RPR.Main_OnCommand(40297, 0) # Unselect all tracks
        self.track.is_selected = True
        
        # Insert the file
        reapy.RPR.InsertMedia(audio_path, 0) 
        
        # Get the item we just inserted
        self.item = self.track.items[-1]
        self.item.length = 600.0 # Make it 10 minutes long
        
        # Set loop source (so it actually loops)
        take = self.item.active_take
        # Use RPR to ensure looping is enabled
        reapy.RPR.SetMediaItemInfo_Value(self.item.id, "B_LOOPSRC", 1)

    def set_frequency(self, val):
        # Map 440-880 Hz to playrate 1.0 to 2.0
        freq = float(val)
        playrate = freq / 440.0
        self.item.set_info_value("D_PLAYRATE", playrate)
        self.label_freq.config(text=f"Freq: {int(freq)} Hz (Rate: {playrate:.2f}x)")

    def set_volume(self, val):
        # Map 0-127 to REAPER volume (0.0 to 1.0)
        vol_midi = float(val)
        vol_real = vol_midi / 127.0
        self.track.set_info_value("D_VOL", vol_real)
        self.label_vol.config(text=f"Vol: {int(vol_midi)}")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Continuous Pitch Instrument")
        self.root.geometry("300x250")

        tk.Label(self.root, text="Continuous Audio Control", font=("Arial", 12, "bold")).pack(pady=10)

        # Frequency
        self.label_freq = tk.Label(self.root, text="Freq: 440 Hz")
        self.label_freq.pack()
        self.slider_freq = tk.Scale(self.root, from_=440, to_=880, orient="horizontal", 
                                     command=self.set_frequency, length=200)
        self.slider_freq.set(440)
        self.slider_freq.pack(pady=5)

        # Volume
        self.label_vol = tk.Label(self.root, text="Vol: 127")
        self.label_vol.pack()
        self.slider_vol = tk.Scale(self.root, from_=0, to_=127, orient="horizontal", 
                                    command=self.set_volume, length=200)
        self.slider_vol.set(127)
        self.slider_vol.pack(pady=5)

    def run(self):
        print("GUI Active. Control frequency and volume in real-time.")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        instr = ContinuousPitchInstrument()
        instr.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
