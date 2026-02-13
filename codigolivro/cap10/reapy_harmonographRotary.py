"""
reapy_harmonographRotary.py

Demonstrates how to create a rotary (3-pendulum) harmonograph
and visualize/sonify it using MIDI CC data in REAPER.

Here, the position is determined by two pendula:
- Circle 1: Freq 8
- Circle 2: Freq 13
Mapping:
- X-Axis -> Pan (CC 10)
- Y-Axis -> Expression (CC 11)

Ported from harmonographRotary.py
"""

import reapy
import math

def map_value(value, in_min, in_max, out_min, out_max):
    # Clamp value to input range to avoid out of bounds CC
    value = max(in_min, min(in_max, value))
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Harmonograph Parameters
    FREQ1 = 8     
    FREQ2 = 13     
    AMPL1 = 40.0   
    AMPL2 = 40.0 

    # We use a lower density than the original py script to avoid freezing REAPER with too many CCs
    # Original density=100. We'll use 10.
    DENSITY = 10.0
    CYCLE_STEPS = int(2 * math.pi * DENSITY)
    CYCLES = 4
    TOTAL_STEPS = CYCLE_STEPS * CYCLES
    
    STEP_QN = 0.05 

    # Create Track
    track = project.add_track()
    track.name = f"Harmonograph Rotary {FREQ1}:{FREQ2}"
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

    print(f"Generating Rotary Harmonograph ({FREQ1}:{FREQ2})...")

    # Insert a single long note
    reapy.RPR.MIDI_InsertNote(take.id, False, False, 0, total_qn, 0, 60, 100, True)

    current_qn = 0.0
    
    # Pre-calc max range for mapping
    # Max possible X = AMPL1 + AMPL2 (constructive interference)
    # Min possible X = -(AMPL1 + AMPL2)
    max_amp = AMPL1 + AMPL2
    
    for i in range(TOTAL_STEPS):
        rotation = i / DENSITY
        
        # Circle 1
        x1 = math.sin(rotation * FREQ1) * AMPL1
        y1 = math.cos(rotation * FREQ1) * AMPL1
        
        # Circle 2
        x2 = math.sin(rotation * FREQ2) * AMPL2
        y2 = math.cos(rotation * FREQ2) * AMPL2
        
        # Combine (Vector subtraction as per original script)
        x = x1 - x2
        y = y1 - y2
        
        # Map X -> Pan (CC 10)
        pan_val = int(map_value(x, -max_amp, max_amp, 0, 127))
        
        # Map Y -> Expression (CC 11)
        expr_val = int(map_value(y, -max_amp, max_amp, 0, 127))
        
        # Insert CCs
        reapy.RPR.MIDI_InsertCC(take.id, False, False, current_qn, 176, 10, pan_val, True)
        reapy.RPR.MIDI_InsertCC(take.id, False, False, current_qn, 176, 11, expr_val, True)
        
        current_qn += STEP_QN

    reapy.RPR.MIDI_Sort(take.id)
    
    # Open Editor
    item.selected = True
    project.perform_action(40153) # Open in MIDI editor
    
    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! Complex rotary patterns generated.")

if __name__ == "__main__":
    main()
