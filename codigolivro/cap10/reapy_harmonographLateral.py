"""
reapy_harmonographLateral.py

Demonstrates how to create a lateral (2-pendulum) harmonograph 
and visualize/sonify it using MIDI CC data in REAPER.

Harmonograph parameters:
- Freq 1: Controls Pan (CC 10)
- Freq 2: Controls Expression (CC 11)

Ported from harmonographLateral.py
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

    # Harmonograph Parameters
    # Freq 1 (Pan) vs Freq 2 (Expression)
    FREQ1 = 2 
    FREQ2 = 3
    AMPL = 1.0 # Normalized amplitude for calc

    DENSITY = 25.0
    CYCLE_STEPS = int(2 * math.pi * DENSITY)
    CYCLES = 6
    TOTAL_STEPS = CYCLE_STEPS * CYCLES
    
    # Duration of each step in QN
    # Make it dense enough to be smooth
    STEP_QN = 0.05 

    # Create Track
    track = project.add_track()
    track.name = f"Harmonograph {FREQ1}:{FREQ2}"
    track.select()
    
    # Calculate Total Length
    bpm = 120
    qn_to_sec = 60 / bpm
    total_qn = TOTAL_STEPS * STEP_QN
    total_sec = total_qn * qn_to_sec

    # Create Item
    item = track.add_item(0, total_sec)
    take = item.active_take
    
    if not take:
        print("Error creating take.")
        return

    print(f"Generating Harmonograph ({FREQ1}:{FREQ2}) data...")

    # Insert a single long note so we can hear the synth
    # Pitch C4 (60), Vel 100
    reapy.RPR.MIDI_InsertNote(take.id, False, False, 0, total_qn, 0, 60, 100, True)

    current_qn = 0.0
    
    # Loop
    for i in range(TOTAL_STEPS):
        rotation = i / DENSITY
        
        # Calculate Sine Waves
        # In original: x = sin(rot * freq1), y = sin(rot * freq2)
        
        # Map X to Pan (CC 10)
        val_x = math.sin(rotation * FREQ1)
        pan_val = int(map_value(val_x, -1.0, 1.0, 0, 127))
        
        # Map Y to Expression (CC 11)
        val_y = math.sin(rotation * FREQ2)
        expr_val = int(map_value(val_y, -1.0, 1.0, 0, 127))
        
        # Insert CCs
        # MIDI_InsertCC(take, selected, muted, time_qn, msg_type (176), cc_num, value, noSort)
        reapy.RPR.MIDI_InsertCC(take.id, False, False, current_qn, 176, 10, pan_val, True)
        reapy.RPR.MIDI_InsertCC(take.id, False, False, current_qn, 176, 11, expr_val, True)
        
        current_qn += STEP_QN

    reapy.RPR.MIDI_Sort(take.id)
    
    # Open Editor
    item.selected = True
    cmd_open_midi = 40153 
    project.perform_action(cmd_open_midi)
    
    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! Check CC Lane 10 (Pan) and 11 (Expression) to see the waves.")

if __name__ == "__main__":
    main()
