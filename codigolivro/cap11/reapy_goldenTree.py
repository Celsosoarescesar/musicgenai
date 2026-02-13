"""
reapy_goldenTree.py

Demonstrates how to generate a "Golden Tree" musical structure using recursion.
The tree branches in time and pitch.
- Time: Each branch starts after its parent.
- Pitch: Left/Right branches diverge in pitch.
- Duration: Scales by the Golden Ratio (Phi) at each level.

Ported from goldenTree.py
"""

import reapy
import math

# Constants
PHI = (math.sqrt(5) - 1) / 2 # approx 0.618
DEPTH = 8
ROOT_PITCH = 60 # C4
INITIAL_DURATION_QN = 4.0 # Whole Note
INTERVAL = 5 # Semitones (Perfect 4th/5th rough interval)

def generate_tree(take, start_qn, duration_qn, pitch, angle, depth):
    """
    Recursively adds notes to the MIDI take.
    """
    if depth == 0:
        return

    # Insert Note for current branch
    # RPR.MIDI_InsertNote(take, selected, muted, start, end, chan, pitch, vel, noSort)
    
    end_qn = start_qn + duration_qn
    vel = 100
    
    # Clamp pitch to valid MIDI range (0-127)
    valid_pitch = max(0, min(127, int(pitch)))
    
    reapy.RPR.MIDI_InsertNote(take.id, False, False, start_qn, end_qn, 0, valid_pitch, vel, True)
    
    # Calculate next generation parameters
    new_duration = duration_qn * PHI
    new_start = end_qn # Branches start where parent ends
    
    # Angle in visual tree affected x/y. Here we affect pitch.
    # We can simulate "angle" as pitch deviation.
    # Left branch: Pitch down
    # Right branch: Pitch up
    # We also reduce the "angle" (interval) slightly or keep it constant?
    # In original: angle - rotation / angle + rotation.
    # Let's keep a constant interval for musical clarity or scale it?
    # Let's scale interval too for fractal-ness? 
    # Or just constant interval is more audible as "branching".
    
    left_pitch = pitch - INTERVAL
    right_pitch = pitch + INTERVAL
    
    # Recurse
    # Left Branch
    generate_tree(take, new_start, new_duration, left_pitch, angle, depth - 1)
    
    # Right Branch
    generate_tree(take, new_start, new_duration, right_pitch, angle, depth - 1)

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Create Track
    track = project.add_track()
    track.name = "Golden Tree"
    track.select()
    
    # Calculate Total Length approx
    # Series: 4 + 4*phi + 4*phi^2 ... geometric series
    # Sum = a * (1 - r^n) / (1 - r) ?
    # approx max length will be sum of durations down one path
    # 4 / (1 - 0.618) approx 10.5 QN
    
    total_qn = INITIAL_DURATION_QN * 10 # ample space
    bpm = 120
    qn_to_sec = 60 / bpm
    total_sec = total_qn * qn_to_sec

    # Create Item
    item = track.add_item(0, total_sec)
    take = item.active_take
    if not take: return

    print(f"Generating Golden Tree (Depth {DEPTH})...")

    # Start Recursion
    # visual angle was 90 deg (Up). Pitch is 60.
    generate_tree(take, 0.0, INITIAL_DURATION_QN, ROOT_PITCH, 90, DEPTH)
    
    reapy.RPR.MIDI_Sort(take.id)
    
    # Open Editor
    item.selected = True
    project.perform_action(40153)
    
    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! Fractal tree generated.")

if __name__ == "__main__":
    main()
