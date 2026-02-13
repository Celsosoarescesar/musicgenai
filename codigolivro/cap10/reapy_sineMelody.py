"""
reapy_sineMelody.py

This program demonstrates how to create a melody from a sine wave.
It maps the sine function to a melodic (i.e., pitch) contour.
It creates a MIDI item in REAPER with the generated notes.

Ported from sineMelody.py
"""

import reapy
import math

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Constants
    DENSITY = 25.0
    CYCLE = int(2 * math.pi * DENSITY)
    NOTE_DURATION = 0.25 # Seconds (approx 16th note at 120bpm, but technically beats in REAPER)
    # in reapy/REAPER time is usually seconds. 
    # But MIDI notes in reapy take start/end in seconds (or beats/QN depending on function).
    # take.add_midi_note uses qn (quarter notes) usually?
    # Actually, reapy's `take.add_midi_note` takes (selected, muted, start, end, chan, pitch, vel)
    # where start and end are in Quarter Notes (QN) if using `RPR.MIDI_InsertNote` 
    # or seconds if using `take.add_note` wrapper?
    # Let's check `reapy` docs logic or standard usage. 
    # Standard reapy `take.add_note` expects start/end in seconds? NO, reapy wrapper usually uses beats/QN?
    # Let's use the low-level RPR.MIDI_InsertNote which uses QN.
    
    QN_DURATION = 0.25 # 16th note

    # MIDI Range
    C2 = 36
    C8 = 108
    TN = QN_DURATION # Duration in QN

    # Create Track
    track = project.add_track()
    track.name = "Sine Melody"
    track.select()

    # Create MIDI Item
    # We need to know length in seconds for the item
    # Assuming 120 BPM, 1 QN = 0.5s.
    bpm = 120 # Default
    qn_to_sec = 60 / bpm
    
    total_qn = CYCLE * QN_DURATION
    total_sec = total_qn * qn_to_sec

    # Add item to track
    # add_item(position=0, length=total_sec)
    item = track.add_item(0, total_sec)
    take = item.active_take
    
    if not take:
        print("Error creating MIDI take.")
        return

    print(f"Generating {CYCLE} notes...")

    # Start a transaction for speed
    # with project.undo_block("Generate Sine Melody"):
    for i in range(CYCLE):
        value = math.sin(i / DENSITY) # calculate sine value
        
        # Map to pitch C2-C8
        pitch = int(map_value(value, -1.0, 1.0, C2, C8))
        
        start_qn = i * QN_DURATION
        end_qn = start_qn + QN_DURATION
        
        start_sec = start_qn * qn_to_sec
        end_sec = end_qn * qn_to_sec
        
        # Use high-level API which takes seconds
        take.add_note(start_sec, end_sec, pitch, 100, 0)

    # Sort MIDI (required after bulk inserts) - High level might handle it, but good to be safe if mixing
    reapy.RPR.MIDI_Sort(take.id)

    # Open in MIDI Editor
    cmd_open_midi = 40153 # Item: Open in built-in MIDI editor
    item.selected = True
    project.perform_action(cmd_open_midi)

    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! Playing melody.")

if __name__ == "__main__":
    main()
