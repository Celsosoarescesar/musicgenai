import reapy
import random

def create_pentatonic_melody():
    # Connect to REAPER
    project = reapy.Project()
    
    # Pentatonic Scale: C4, D4, E4, G4, A4
    pentatonic_scale = [60, 62, 64, 67, 69]
    # Durations in beats: QN=1.0, DEN=0.75, EN=0.5, SN=0.25
    durations = [1.0, 0.75, 0.5, 0.25]
    
    # Pick a random number of notes to create (between 12 and 18)
    num_notes = random.randint(12, 18)
    
    melody_data = [] # List of (pitch, duration)
    
    # 1. First note should be root (C4)
    melody_data.append((60, 1.0))
    
    # 2. Generate intermediate random notes
    for _ in range(num_notes - 2):
        pitch = random.choice(pentatonic_scale)
        duration = random.choice(durations)
        velocity = random.randint(80, 120)
        # Note: we'll store velocity here too
        melody_data.append((pitch, duration, velocity))
        
    # 3. Last note should be root also (a half note, to signify end)
    melody_data.append((60, 2.0, 100)) # Pitch 60, Duration 2.0 (HN), Velocity 100
    
    # REAPER Integration
    track = project.add_track(name="Pentatonic Melody")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.01 # Plucky attack
        synth.params[2] = 0.5  # Medium decay
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    total_beats = sum(n[1] for n in melody_data)
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Random Pentatonic Melody"
    take = item.active_take
    
    current_beat = 0.0
    for note_info in melody_data:
        pitch = note_info[0]
        dur = note_info[1]
        vel = note_info[2] if len(note_info) > 2 else 100
        
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + dur * 0.9) * spb),
            velocity=int(vel),
            channel=0
        )
        current_beat += dur

    print(f"Pentatonic melody with {num_notes} notes generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_pentatonic_melody()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
