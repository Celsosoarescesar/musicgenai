"""
reapy_sliderControl.py

Demonstrates how to create a simple slider control surface using Tkinter
that controls REAPER parameters in real-time.

It allows controlling the Master Volume and Pan from an external window.

Ported from sliderControl.py
"""

import reapy
import tkinter as tk

class SliderControl:
    def __init__(self, root, title="Slider", update_function=None, 
                 min_value=0, max_value=100, start_value=None):
        """Initializes a SliderControl object using Tkinter Scale."""
        
        self.update_function = update_function
        
        if start_value is None:
            start_value = (min_value + max_value) / 2
            
        # UI Frame
        frame = tk.Frame(root, pady=10)
        frame.pack(fill=tk.X)
        
        # Label
        self.label = tk.Label(frame, text=title)
        self.label.pack()
        
        # Slider
        self.slider = tk.Scale(
            frame, 
            from_=min_value, 
            to=max_value, 
            orient=tk.HORIZONTAL,
            command=self.on_change,
            resolution=0.01 # Float precision
        )
        self.slider.set(start_value)
        self.slider.pack(fill=tk.X, padx=20)
        
    def on_change(self, value):
        """Called when slider moves."""
        val = float(value)
        if self.update_function:
            self.update_function(val)

def main():
    # 1. Connect to REAPER
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # 2. Define Callback Functions
    
    def set_master_volume(value):
        # Value 0 to 100. REAPER Vol is linear-ish gain or dB?
        # reapy volume is usually linear gain (1.0 = 0dB).
        # Let's map 0-100 to 0.0-1.0
        vol = value / 100.0
        project.master_track.volume = vol
        print(f"Master Volume: {vol:.2f}")

    def set_master_pan(value):
        # Value -1.0 to 1.0 (Left to Right)
        # Slider can be -100 to 100
        pan = value / 100.0
        project.master_track.pan = pan
        print(f"Master Pan: {pan:.2f}")
        
    def print_value(value):
        print(f"Test Slider: {value}")

    # 3. Create GUI
    root = tk.Tk()
    root.title("REAPER Control Surface")
    root.geometry("300x250")
    
    label = tk.Label(root, text="Chapter 13: External Control", font=("Arial", 12, "bold"))
    label.pack(pady=10)

    # Slider 1: Master Volume
    # Get current vol?
    current_vol = project.master_track.volume * 100
    SliderControl(root, "Master Volume (0-100%)", set_master_volume, 0, 100, current_vol)

    # Slider 2: Master Pan
    current_pan = project.master_track.pan * 100
    SliderControl(root, "Master Pan (L/R)", set_master_pan, -100, 100, current_pan)

    # Slider 3: Test
    SliderControl(root, "Test Print", print_value, 0, 10, 5)

    print("Starting GUI... (Close window to exit)")
    root.mainloop()

if __name__ == "__main__":
    main()
