"""
reapy_sierpinskiTriangle.py

Demonstrates how to generate a Sierpinski Triangle musical structure using recursion.
The visual structure is mapped to the piano roll:
- X-Axis: Time
- Y-Axis: Pitch

Result: The MIDI notes technically form a Sierpinski Triangle image.

Ported from sierpinskiTriangle.py
"""

import reapy

# Constants
DEPTH = 6
TOTAL_DURATION_QN = 16.0 # 4 bars of 4/4
MIN_PITCH = 48 # C3
MAX_PITCH = 84 # C6 (3 Octaves range)

# We define the triangle "space" as 0.0 to 1.0
# Then we map to Time/Pitch

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def insert_note_at_point(take, x_norm, y_norm, depth):
    # Map X (0..1) to Time QN
    time_qn = map_value(x_norm, 0.0, 1.0, 0.0, TOTAL_DURATION_QN)
    
    # Map Y (0..1) to Pitch
    # Y=1.0 is TOP (High Pitch), Y=0.0 is BOTTOM (Low Pitch)
    # Actually in Py GUI, Y=0 is top. We inverted logic in recursion?
    # Let's assume input y_norm is consistent such that 1.0 = High Pitch Concept.
    pitch = int(map_value(y_norm, 0.0, 1.0, MIN_PITCH, MAX_PITCH))
    pitch = max(0, min(127, pitch))
    
    # Duration based on depth (Depper = smaller triangle = shorter note)
    # Base duration
    dur = 0.5 / depth # arbitrary scaling
    
    reapy.RPR.MIDI_InsertNote(take.id, False, False, time_qn, time_qn + dur, 0, pitch, 100, True)

def sierpinski(take, x, y, w, h, depth):
    """
    x, y: Coordinates of the TOP vertex of the current sub-triangle.
    w: Width of base
    h: Height of triangle
    
    Coordinate System:
    y = 1.0 is TOP (Highest Pitch)
    y = 0.0 is BOTTOM (Lowest Pitch)
    """
    
    if depth == 1:
        # Leaf Node: Draw the triangle by placing notes at vertices
        # Top Vertex
        insert_note_at_point(take, x, y, DEPTH)
        # Left Bottom
        insert_note_at_point(take, x - w/2, y - h, DEPTH)
        # Right Bottom
        insert_note_at_point(take, x + w/2, y - h, DEPTH)
    else:
        # Subdivide
        # Top Sub-triangle
        # Top vertex is same: x, y
        # New Width = w/2, New Height = h/2
        sierpinski(take, x, y, w/2, h/2, depth - 1)
        
        # Left Sub-triangle
        # Top vertex is at middle of left edge of current triangle
        # Left edge goes from (x, y) to (x - w/2, y - h)
        # Midpoint is (x - w/4, y - h/2)
        sierpinski(take, x - w/4, y - h/2, w/2, h/2, depth - 1)
        
        # Right Sub-triangle
        # Top vertex is at middle of right edge
        # Midpoint is (x + w/4, y - h/2)
        sierpinski(take, x + w/4, y - h/2, w/2, h/2, depth - 1)

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Create Track
    track = project.add_track()
    track.name = "Sierpinski Triangle"
    track.select()
    
    bpm = 120
    qn_to_sec = 60 / bpm
    total_sec = TOTAL_DURATION_QN * qn_to_sec

    # Create Item
    item = track.add_item(0, total_sec)
    take = item.active_take
    if not take: return

    print(f"Generating Sierpinski Cloud (Depth {DEPTH})...")

    # Initial Triangle parameters (Normalized 0..1)
    # Center X = 0.5
    # Top Y = 1.0
    # Width = 1.0 (spanning 0.0 to 1.0 at base? no base is wider? let's stick to safe bounds)
    # Let's say Width = 0.8
    # Height = 0.8
    
    sierpinski(take, 0.5, 0.9, 0.8, 0.8, DEPTH)
    
    reapy.RPR.MIDI_Sort(take.id)
    
    # Open Editor
    item.selected = True
    project.perform_action(40153)
    
    reapy.RPR.CSurf_OnPlay()
    print("Done! Musical fractal generated.")

if __name__ == "__main__":
    main()
