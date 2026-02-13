import reapy
import random

def create_pierre_cage_structures():
    # Connect to REAPER
    project = reapy.Project()
    
    number_of_notes = 100
    
    # Ranges
    # MIDI Pitches: C1 (24) to C7 (96)
    # Dynamics (Velocity): PP (32) to FFF (127)
    
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat

    def generate_random_melody(track_name):
        track = project.add_track(name=track_name)
        synth = track.add_fx("ReaSynth")
        if synth:
            # Randomize some synth params for variety if desired
            synth.params[1] = 0.01 # Fast attack
            synth.params[2] = random.uniform(0.1, 0.8) # Random decay
            
        # First, we need to know the total duration to create the MIDI item
        # We'll pre-calculate the notes to find the end time
        notes_to_add = []
        current_time = 0.0
        for _ in range(number_of_notes):
            pitch = random.randint(24, 96) # C1 to C7
            duration = random.random() * 1.0 # 0.0 to 1.0 beats
            velocity = random.randint(32, 127) # PP to FFF
            
            notes_to_add.append({
                "pitch": pitch,
                "start": current_time,
                "end": current_time + duration,
                "vel": velocity
            })
            current_time += duration
            
        # Create MIDI item covering the whole random duration
        item = track.add_midi_item(0, end=current_time * spb)
        item.name = f"{track_name} Aleatoric"
        take = item.active_take
        
        # Add the notes
        for note in notes_to_add:
            take.add_note(
                pitch=int(note["pitch"]),
                start=float(note["start"] * spb),
                end=float(note["end"] * spb),
                velocity=int(note["vel"]),
                channel=0
            )
        
        return current_time

    # Generate both melodies starting at the same time
    print(f"Generating {number_of_notes} random notes for Piano Boulez...")
    len1 = generate_random_melody("Piano Boulez")
    
    print(f"Generating {number_of_notes} random notes for Piano Cage...")
    len2 = generate_random_melody("Piano Cage")

    print(f"Aleatoric structures generated. Total durations: Boulez={len1:.2f}s, Cage={len2:.2f}s.")

if __name__ == "__main__":
    try:
        create_pierre_cage_structures()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
