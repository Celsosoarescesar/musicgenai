import reapy

def note_to_midi(note_str):
    """Converts a note string like 'C4' or 'Eb3' to a MIDI number."""
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 
             'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 
             'A#': 10, 'Bb': 10, 'B': 11}
    
    note_str = note_str.strip().capitalize()
    if len(note_str) < 2:
        return 60 # Default to C4
    
    # Handle accidentals
    if len(note_str) > 2 and (note_str[1] == '#' or note_str[1] == 'b'):
        name = note_str[:2]
        octave_str = note_str[2:]
    else:
        name = note_str[0]
        octave_str = note_str[1:]
        
    try:
        octave = int(octave_str)
        pitch = (octave + 1) * 12 + notes[name]
        return pitch
    except (ValueError, KeyError):
        return 60 # Fallback to C4

def create_relative_arpeggio():
    # Connect to REAPER
    project = reapy.Project()
    
    # Relative intervals for a major chord (Root, Major 3rd, Perfect 5th, Octave...)
    arpeggio_pattern = [0, 4, 7, 12, 7, 4]
    
    # TN (Thirty-second Note) duration in beats
    duration = 0.125 
    
    # User Inputs
    root_str = input("Enter root note (e.g., C4, Eb3, F#4): ")
    root_pitch = note_to_midi(root_str)
    
    try:
        user_input_reps = input("How many times to repeat arpeggio: ")
        repetitions = int(user_input_reps)
    except ValueError:
        print("Invalid repetition input. Using default (2).")
        repetitions = 2
    
    # REAPER Setup
    track = project.add_track(name=f"Arpeggio on {root_str}")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.0 # Fast attack
        synth.params[2] = 0.4 # Short decay
        synth.params[3] = 0.0 # No sustain
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    # Calculate total length
    one_repeat_beats = len(arpeggio_pattern) * duration
    total_beats = (one_repeat_beats * repetitions) + (duration * 4) # Pattern + final long note (4x duration)
    
    # Create MIDI item
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = f"Arpeggio {root_str} Take"
    take = item.active_take
    
    current_beat = 0.0
    
    # Add repeated pattern
    for _ in range(repetitions):
        for interval in arpeggio_pattern:
            take.add_note(
                pitch=int(root_pitch + interval),
                start=float(current_beat * spb),
                end=float((current_beat + duration * 0.9) * spb),
                velocity=100,
                channel=0
            )
            current_beat += duration
            
    # Add final note (close with first pitch, much longer duration)
    last_pitch = root_pitch + arpeggio_pattern[0]
    final_duration = duration * 4
    take.add_note(
        pitch=int(last_pitch),
        start=float(current_beat * spb),
        end=float((current_beat + final_duration * 0.9) * spb),
        velocity=100,
        channel=0
    )

    print(f"Relative Arpeggiator generated in REAPER on {root_str} with {repetitions} repetitions.")

if __name__ == "__main__":
    try:
        create_relative_arpeggio()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
