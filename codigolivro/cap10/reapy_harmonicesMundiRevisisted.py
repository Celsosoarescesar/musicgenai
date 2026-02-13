"""
reapy_harmonicesMundiRevisisted.py

Sonify mean planetary velocities in the solar system.
Creates 9 tracks in REAPER, one for each planet.

Ported from harmonicesMundiRevisisted.py
"""

import reapy
import math
import random

# Constants
# Notes
C3 = 48
C4 = 60
C6 = 84

# Scale Intervals (Mixolydian)
MIXOLYDIAN_INTERVALS = [0, 2, 4, 5, 7, 9, 10, 12]

# Durations (QN)
SN = 0.25
QN = 1.0
DURATIONS = [SN, QN]

# Planets Data
# Mercury, Venus, Earth, Mars, Ceres, Jupiter, Saturn, Uranus, Neptune
PLANET_VELOCITIES = [47.89, 35.03, 29.79, 24.13, 17.882, 13.06, 9.64, 6.81, 5.43]
PLANET_NAMES = ["Mercury", "Venus", "Earth", "Mars", "Ceres", "Jupiter", "Saturn", "Uranus", "Neptune"]

MIN_VELOCITY = min(PLANET_VELOCITIES)
MAX_VELOCITY = max(PLANET_VELOCITIES)

SPEED_FACTOR = 0.01
NUM_NOTES = 100

def map_value(value, in_min, in_max, out_min, out_max):
    val = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(out_min, min(out_max, val)) # Clamp

def get_scale_notes(root, intervals, bottom_midi, top_midi):
    """Generates a list of valid MIDI notes in the scale within range."""
    notes = []
    # Start usually from C0 (12) or so
    # Simple generation: check all MIDI notes
    for midi_note in range(bottom_midi, top_midi + 1):
        # Calculate interval from root (modulo 12)
        # root is C4 (60) usually, or we can just say Scale Root C (0, 12, 24...).
        # Assuming C Mixolydian.
        # Note % 12 should be in [(root + i) % 12 for i in intervals]
        # If root is C (0), intervals are absolute mod 12.
        
        # Let's assume Scale is C Mixolydian.
        root_class = root % 12
        note_class = midi_note % 12
        interval_class = (note_class - root_class) % 12
        
        if interval_class in MIXOLYDIAN_INTERVALS:
            notes.append(midi_note)
    return notes

def map_to_scale(value, in_min, in_max, scale_notes):
    """Maps continuous value to nearest note in scale list."""
    # Map value to index in scale_notes
    num_notes = len(scale_notes)
    if num_notes == 0: return 60 # Default
    
    idx = int(map_value(value, in_min, in_max, 0, num_notes - 1))
    return scale_notes[idx]

def sonify_planet(project, index, velocity, name):
    print(f"Sonifying {name} (Vel: {velocity})...")
    
    # Create Track
    track = project.add_track()
    track.name = f"{name} ({velocity})"
    
    # Scale Notes for Mapping (C3 to C6)
    scale_notes = get_scale_notes(C4, MIXOLYDIAN_INTERVALS, C3, C6)
    
    # Generate Note Data
    current_qn = 0.0
    
    # Store events to write in bulk if possible, or just sequential write
    # We need total length for item first? 
    # Since durations are random, we calculate logic first.
    
    note_events = []
    total_qn = 0.0
    
    for i in range(NUM_NOTES):
        # Pitch is constant for the planet in original code logic:
        # pitch = mapScale(planetVelocity...) -> Based on Planet Velocity which is const for the loop
        
        pitch = map_to_scale(velocity, MIN_VELOCITY, MAX_VELOCITY, scale_notes)
        
        # Duration
        dur = random.choice(DURATIONS)
        
        # Dynamics & Pan oscillate
        # pan = mapValue(sin(i * planetVelocity * speedFactor * 2)...)
        pan_osc = math.sin(i * velocity * SPEED_FACTOR * 2)
        pan = int(map_value(pan_osc, -1.0, 1.0, 0, 127))
        
        # dyn = mapValue(cos(i * planetVelocity * speedFactor * 3)...)
        dyn_osc = math.cos(i * velocity * SPEED_FACTOR * 3)
        dyn = int(map_value(dyn_osc, -1.0, 1.0, 40, 127))
        
        note_events.append({
            "start": current_qn,
            "end": current_qn + dur,
            "pitch": pitch,
            "vel": dyn,
            "pan": pan
        })
        
        current_qn += dur
        
    total_qn = current_qn
    
    # BPM to seconds
    bpm = 120
    qn_to_sec = 60 / bpm
    total_sec = total_qn * qn_to_sec
    
    # Create Item
    item = track.add_item(0, total_sec)
    take = item.active_take
    if not take: return
    
    # Write Events
    for evt in note_events:
        # Note
        reapy.RPR.MIDI_InsertNote(take.id, False, False, evt["start"], evt["end"], 0, evt["pitch"], evt["vel"], True)
        
        # Pan CC (10)
        reapy.RPR.MIDI_InsertCC(take.id, False, False, evt["start"], 176, 10, evt["pan"], True)

    reapy.RPR.MIDI_Sort(take.id)

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Create distinct random seed for variety if run multiple times? 
    # Logic is deterministic mostly except duration.
    
    # Process each planet
    for i, velocity in enumerate(PLANET_VELOCITIES):
        name = PLANET_NAMES[i]
        sonify_planet(project, i, velocity, name)
        
    # Play
    reapy.RPR.CSurf_OnPlay()
    print("Done! 9 Planets sonified.")

if __name__ == "__main__":
    main()
