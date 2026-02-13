import reapy
import random

def create_wind_chimes():
    # Connect to REAPER
    project = reapy.Project()
    
    # Program parameters
    cycles = 24       # how many times striker hits all four tubes
    max_duration = 8.0 # max duration in beats
    min_vol = 80       # MIDI velocity limits
    max_vol = 100
    
    # Tube tuning (MIDI numbers)
    tubes = [60, 65, 55, 74] # C5, F5, G4, D6
    offsets = [0.0, 1.0, 3.0, 5.0] # Initial delay for each tube in beats
    
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    # REAPER Integration
    track = project.add_track(name="Wind Chimes (Ambient)")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Bell-like configuration
        synth.params[1] = 0.005 # Instant attack
        synth.params[2] = 2.0   # Long decay for bells
        synth.params[3] = 0.0   # No sustain
        
    # We'll calculate all notes first to find the total end time
    all_notes = []
    
    for tube_pitch, start_offset_beats in zip(tubes, offsets):
        current_beat = start_offset_beats
        for _ in range(cycles):
            note_duration_beats = random.random() * max_duration
            velocity = random.randint(min_vol, max_vol)
            
            all_notes.append({
                "pitch": tube_pitch,
                "start": current_beat,
                "end": current_beat + note_duration_beats,
                "vel": velocity
            })
            # In the original script, notes are added sequentially to each phrase
            current_beat += note_duration_beats
            
    # Find the maximum end time for the MIDI item
    max_beat = max(n["end"] for n in all_notes) if all_notes else 10.0
    
    # Create the MIDI item
    item = track.add_midi_item(0, end=max_beat * spb)
    item.name = "Wind Chimes Simulation"
    take = item.active_take
    
    # Add all generated notes
    for note in all_notes:
        take.add_note(
            pitch=int(note["pitch"]),
            start=float(note["start"] * spb),
            end=float(note["end"] * spb),
            velocity=int(note["vel"]),
            channel=0
        )
        
    print(f"Wind Chimes simulation generated in REAPER with {len(all_notes)} strikes.")

if __name__ == "__main__":
    try:
        create_wind_chimes()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
