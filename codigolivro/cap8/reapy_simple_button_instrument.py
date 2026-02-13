import reapy
import tkinter as tk

def setup_reaper_track():
    """Sets up a track in REAPER for real-time playback."""
    project = reapy.Project()
    
    # Check if track already exists, or create it
    track_name = "Simple Button Instrument"
    target_track = None
    for track in project.tracks:
        if track.name == track_name:
            target_track = track
            break
            
    if not target_track:
        target_track = project.add_track(name=track_name)
        target_track.add_fx("ReaSynth")
        
    # Arm for recording and turn on monitoring so we can hear it
    target_track.is_armed = True
    # monitoring = 1 is ON
    # In reapy, track.set_info_value("I_RECMON", 1)
    target_track.set_info_value("I_RECMON", 1)
    
    return project

def start_note(pitch=69):
    # Using REAPER's StuffMIDIMessage (mode 0 = Virtual MIDI Keyboard)
    # 0x90 is Note On, 0x80 is Note Off
    # channel 1 (0x90)
    reapy.RPR.StuffMIDIMessage(0, 0x90, pitch, 100)

def stop_note(pitch=69):
    # Send Note Off
    reapy.RPR.StuffMIDIMessage(0, 0x80, pitch, 0)

def stop_all_notes():
    # Loop through a reasonable range and send Note Off
    # REAPER doesn't have a single "All Notes Off" StuffMIDIMessage shorthand
    # but we can send a CC 123 to channel 1
    reapy.RPR.StuffMIDIMessage(0, 0xB0, 123, 0)

def run_button_instrument():
    # 1. Setup REAPER
    try:
        project = setup_reaper_track()
    except Exception as e:
        print(f"Error connecting to REAPER: {e}")
        print("Ensure REAPER is open and reapy is configured.")
        return

    # 2. Setup GUI
    root = tk.Tk()
    root.title("Simple Button Instrument")
    root.geometry("300x150")

    pitch = 69 # A4

    # Callback wrappers
    def on_click():
        start_note(pitch)
        status_label.config(text=f"Note ON: {pitch}")

    def off_click():
        stop_note(pitch)
        status_label.config(text="Note OFF")

    # Widgets
    btn_on = tk.Button(root, text="ON", command=on_click, width=10, height=2, bg="lightgreen")
    btn_on.pack(pady=10)

    btn_off = tk.Button(root, text="OFF", command=off_click, width=10, height=2, bg="lightcoral")
    btn_off.pack(pady=5)

    status_label = tk.Label(root, text="Ready")
    status_label.pack(side="bottom", pady=5)

    print("Instrument GUI active. Click buttons to play.")
    root.mainloop()

if __name__ == "__main__":
    run_button_instrument()
