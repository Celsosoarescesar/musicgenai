"""
reapy_clementine.py

Demonstrates how to create a musical instrument using an OSC device (accelerometer).
It receives OSC messages from device accelerometer and gyroscope.

Setup:
- Use an OSC app (like TouchOSC) sending Accelerometer data to port 57110.
- Address: /accxyz
- Args: [x, y, z] (Floats)

Mapping:
- Y-Axis (Pitch): Controls the pitch (Major Scale).
- X-Axis (Roll): Triggers a note if tilted enough.
- Z-Axis (Shake): Controls velocity/loudness.

Ported from clementine.py (randomCirclesThroughOSCInput.py)
"""

import reapy
import time
import sys
import random
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# Constants
TRIGGER_THRESHOLD = 0.3
NOTE_ON = 0x90
NOTE_OFF = 0x80
COOLDOWN = 0.2 # Seconds between notes

# Scale (Major) - Relative semitones
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11, 12]
BASE_NOTE = 60 # C4

last_note_time = 0

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_scale_note(pitch_val):
    """
    Maps a pitch value (-1.0 to 1.0) to a note in the Major Scale.
    We'll span about 2 octaves.
    """
    # Map -1.0..1.0 to index 0..15 (approx 2 octaves)
    scale_len = len(MAJOR_SCALE_INTERVALS)
    octaves = 2
    total_notes = scale_len * octaves
    
    # Clamp pitch_val
    pitch_val = max(-1.0, min(1.0, pitch_val))
    
    # Map to index
    note_idx = int(map_value(pitch_val, -1.0, 1.0, 0, total_notes - 1))
    
    # Calculate MIDI note
    octave_offset = note_idx // scale_len
    interval_idx = note_idx % scale_len
    
    note_num = BASE_NOTE + (octave_offset * 12) + MAJOR_SCALE_INTERVALS[interval_idx]
    return int(note_num)

def process_accel(address, *args):
    """
    Callback for /accxyz
    Args usually: [x, y, z] (or similar, depending on app)
    Target:
    - roll (x) -> Trigger
    - pitch (y) -> Note
    - shake (z) -> Velocity
    """
    global last_note_time

    if len(args) < 3:
        return

    roll = args[0]
    pitch_val = args[1]
    shake_val = args[2]

    # Check cooldown
    current_time = time.time()
    if current_time - last_note_time < COOLDOWN:
        return

    # Check Trigger (Roll)
    if abs(roll) > TRIGGER_THRESHOLD:
        last_note_time = current_time
        
        # Calculate Params
        note = get_scale_note(pitch_val)
        
        # Shake usually is 1g (approx 1.0) +/- shake. 
        # Let's map magnitude of Shake to velocity.
        # Assuming Z is gravity + shake. simple abs mapping.
        # Range approx 0.8 to 3.0 in original script
        val_abs = abs(shake_val)
        velocity = int(map_value(val_abs, 0.5, 3.0, 50, 127))
        velocity = max(0, min(127, velocity))

        # Play Note
        # We send Note On, sleep briefly, then Note Off to simulate a "plucked" or triggered sound
        # that doesn't hang forever.
        
        status_on = NOTE_ON | 0 # Channel 1
        reapy.RPR.StuffMIDIMessage(0, status_on, note, velocity)
        print(f"Trigger! Note: {note} Vel: {velocity} (Roll: {roll:.2f} Pitch: {pitch_val:.2f})")
        
        # Optional: Blocking sleep to define note length. 
        # Since this is a Blocking Server, this will delay next sensor reading, 
        # effectively rate limiting "machine gun" notes too.
        time.sleep(0.1) 
        
        status_off = NOTE_OFF | 0
        reapy.RPR.StuffMIDIMessage(0, status_off, note, 0)

def main():
    try:
        # Check connection
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    ip = "0.0.0.0"
    port = 57110

    dispatcher = Dispatcher()
    dispatcher.map("/accxyz", process_accel)

    server = BlockingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving at {ip}:{port}")
    print("Listening for OSC messages on /accxyz (Args: x, y, z)")
    print("Hold your device like an airplane!")
    print(" - Roll (tilt stick L/R) to play notes.")
    print(" - Pitch (nose up/down) to change pitch.")
    print(" - Shake (Z-axis) for volume.")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OSC Server...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
