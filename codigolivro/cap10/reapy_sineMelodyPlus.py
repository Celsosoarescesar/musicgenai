"""
reapy_sineMelodyPlus.py

This program demonstrates how to create a melody from a sine wave.
It maps the sine function to several musical parameters:
- Pitch contour
- Duration (Note length)
- Dynamics (Velocity)
- Panning (CC 10)

Ported from sineMelodyPlus.py
"""

import reapy
import math

# Constants
TN = 0.125 # 32nd note (approx, usually TN is 32nd, SN is 16th? Or 8th/16th? 
# Jython Music: TN = Thirty-second note? No, TN usually means Tenth Note? 
# Actually JythonMusic constants:
# WN = 4.0 (Whole)
# HN = 2.0 (Half)
# QN = 1.0 (Quarter)
# EN = 0.5 (Eighth)
# SN = 0.25 (Sixteenth)
# TN = 0.125 (Thirty-second)
# We will use REAPER QN units where 1.0 = Quarter Note.
QN_DURATION = 1.0 
SN_DURATION = 0.25 # Sixteenth
TN_DURATION = 0.125 # Thirty-second

PAN_LEFT = 0
PAN_RIGHT = 127
PIANISSIMO = 20
FORTISSIMO = 120

C2 = 36
C8 = 108

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    DENSITY = 25.0
    CYCLE = int(2 * math.pi * DENSITY)
    
    # Create Track
    track = project.add_track()
    track.name = "Sine Melody Plus"
    track.select()
    
    # Calculate Total Length (since duration is variable, we need to pre-calc or just make it big enough)
    # Let's pre-calculate to be precise.
    total_qn = 0
    notes_data = [] # Store tuple: (pitch, duration, velocity, pan)
    
    for i in range(CYCLE):
        value = math.sin(i / DENSITY)
        
        pitch = int(map_value(value, -1.0, 1.0, C2, C8))
        duration = map_value(value, -1.0, 1.0, TN_DURATION, SN_DURATION)
        velocity = int(map_value(value, -1.0, 1.0, PIANISSIMO, FORTISSIMO))
        panning = int(map_value(value, -1.0, 1.0, PAN_LEFT, PAN_RIGHT))
        
        notes_data.append({
            "pitch": pitch,
            "dur": duration,
            "vel": velocity,
            "pan": panning
        })
        total_qn += duration

    # Create MIDI Item
    # Convert QN to Seconds (assuming 120 BPM)
    bpm = 120
    qn_to_sec = 60 / bpm
    total_sec = total_qn * qn_to_sec
    
    item = track.add_item(0, total_sec)
    take = item.active_take
    
    if not take:
        print("Error creating take.")
        return

    print(f"Generating {CYCLE} notes with modulation...")

    current_qn = 0.0
    
    # Batch Insert
    # We use RPR directly for CC and Notes to ensure sync
    
    for note in notes_data:
        start_qn = current_qn
        end_qn = current_qn + note["dur"]
        
        # Insert Note
        # RPR.MIDI_InsertNote(take, selected, muted, start_qn, end_qn, chan, pitch, vel, noSort)
        reapy.RPR.MIDI_InsertNote(take.id, False, False, start_qn, end_qn, 0, note["pitch"], note["vel"], True)
        
        # Insert CC 10 (Pan)
        # RPR.MIDI_InsertCC(take, selected, muted, time_qn, msg_type, msg2, msg3, noSort)
        # msg_type 0xB0 (176) = CC. msg2 = CC#, msg3 = Value
        reapy.RPR.MIDI_InsertCC(take.id, False, False, start_qn, 176, 10, note["pan"], True)
        
        current_qn += note["dur"]

    reapy.RPR.MIDI_Sort(take.id)
    
    # Open Editor
    item.selected = True
    cmd_open_midi = 40153 
    project.perform_action(cmd_open_midi)
    
    # Open CC Lane for Pan (CC 10) - Optional, hard to force via API generally, 
    # but user can see it if they select the lane.
    
    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! Playing modulated melody.")

if __name__ == "__main__":
    main()
