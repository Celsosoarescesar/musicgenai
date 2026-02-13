import reapy
from reapy import reascript_api as rpr

def create_piano_phase():
    # Connect to REAPER
    project = reapy.Project()
    
    # Musical parameters
    # E4, FS4, B4, CS5, D5, FS4, E4, CS5, B4, FS4, D5, CS5
    pitches = [64, 66, 71, 73, 74, 66, 64, 73, 71, 66, 74, 73]
    repeats = 41
    sn_duration = 0.25  # A 16th note in beats (quarter note = 1.0)
    
    # Phasing parameters
    tempo1 = 100.0
    tempo2 = 100.5
    
    # Piano 1
    track1 = project.add_track(name="Piano 1")
    # Add ReaSynth and configure it to sound a bit more like a piano (percussive)
    synth1 = track1.add_fx("ReaSynth")
    # ReaSynth parameters (approximate): 0=Vol, 1=Attack, 2=Decay, 3=Sustain, 4=Release
    # Attack: 0.0 (fast), Decay: 2.0s, Sustain: -inf (0.0), Release: 0.1s
    if synth1:
        synth1.params[1] = 0.0    # Attack
        synth1.params[2] = 0.6    # Decay (scaled 0-1, 0.6 is roughly 2s)
        synth1.params[3] = 0.0    # Sustain (0.0 means no sustain)
    # Time in beats for 100 BPM
    # We'll just use beats since REAPER MIDI items handle tempo
    # But wait, Piano 2 needs to drift. 
    # reapy's track.add_midi_item takes start and end in seconds.
    
    def insert_phrase(track, tempo, name):
        # Seconds per quarter note
        spqn = 60.0 / tempo
        # Seconds per 16th note (SN)
        spsn = spqn * 0.25
        
        total_notes = len(pitches) * repeats
        total_duration = total_notes * spsn
        
        # Create MIDI item
        item = track.add_midi_item(0, total_duration)
        item.name = name
        take = item.active_take
        
        # Insert notes
        for r in range(repeats):
            for i, pitch in enumerate(pitches):
                start_time = (r * len(pitches) + i) * spsn
                end_time = start_time + spsn * 0.9
                # Explicitly cast to int for pitch, velocity, and channel to avoid TypeErrors
                take.add_note(
                    pitch=int(pitch), 
                    start=start_time, 
                    end=end_time, 
                    velocity=100, 
                    channel=0
                )
                
    insert_phrase(track1, tempo1, "Phase 1")
    
    # Piano 2
    track2 = project.add_track(name="Piano 2")
    synth2 = track2.add_fx("ReaSynth")
    if synth2:
        synth2.params[1] = 0.0
        synth2.params[2] = 0.6
        synth2.params[3] = 0.0
    insert_phrase(track2, tempo2, "Phase 2 (Drifting)")

    print("Piano Phase generated successfully in REAPER.")

if __name__ == "__main__":
    try:
        create_piano_phase()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure REAPER is open and reapy is correctly configured.")
