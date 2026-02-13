import reapy

def note_to_midi(note_str):
    """Converts a note string like 'C4' or 'Eb3' to a MIDI number."""
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 
             'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 
             'A#': 10, 'Bb': 10, 'B': 11}
    
    note_str = note_str.strip().capitalize()
    if len(note_str) < 2: return 60
    
    if len(note_str) > 2 and (note_str[1] == '#' or note_str[1] == 'b'):
        name, octave_str = note_str[:2], note_str[2:]
    else:
        name, octave_str = note_str[0], note_str[1:]
        
    try:
        return (int(octave_str) + 1) * 12 + notes[name]
    except (ValueError, KeyError):
        return 60

def midi_to_note(midi_num):
    """Converts a MIDI number like 60 to a note string like 'C4'."""
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_num // 12) - 1
    name = names[midi_num % 12]
    return f"{name}{octave}"

def create_scale_tutor():
    # Define Scale Intervals
    scales = {
        "major": [0, 2, 4, 5, 7, 9, 11, 12],
        "minor": [0, 2, 3, 5, 7, 8, 10, 12],
        "dorian": [0, 2, 3, 5, 7, 9, 10, 12],
        "phrygian": [0, 1, 3, 5, 7, 8, 10, 12],
        "lydian": [0, 2, 4, 6, 7, 9, 11, 12],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
        "locrian": [0, 1, 3, 5, 6, 8, 10, 12],
        "pentatonic": [0, 2, 4, 7, 9, 12]
    }
    
    print("This program outputs the pitches of a scale and plays them in REAPER.")
    
    scale_name = input(f"Enter scale (Options: {', '.join(scales.keys())}): ").lower().strip()
    if scale_name not in scales:
        print(f"Unknown scale '{scale_name}'. Defaulting to major.")
        scale_name = "major"
        
    root_str = input("Enter root note (e.g., C4): ").strip()
    root_midi = note_to_midi(root_str)
    
    # Calculate scale pitches
    intervals = scales[scale_name]
    scale_pitches = [root_midi + i for i in intervals]
    scale_names = [midi_to_note(p) for p in scale_pitches]
    
    print(f"\nThe notes in {root_str} {scale_name} are: {', '.join(scale_names)}.")
    
    # REAPER Integration
    try:
        project = reapy.Project()
        track = project.add_track(name=f"Scale Tutor: {root_str} {scale_name}")
        synth = track.add_fx("ReaSynth")
        
        tempo = project.bpm
        if not tempo or tempo == 0: tempo = 120.0
        spb = 60.0 / tempo
        
        # Create MIDI item
        duration = 1.0 # 1 beat per note
        total_beats = len(scale_pitches) * duration
        item = track.add_midi_item(0, end=total_beats * spb)
        item.name = f"{root_str} {scale_name} Scale"
        take = item.active_take
        
        for i, pitch in enumerate(scale_pitches):
            take.add_note(
                pitch=int(pitch),
                start=float(i * duration * spb),
                end=float((i * duration + 0.8) * spb),
                velocity=100,
                channel=0
            )
        print("\nScale generated in REAPER successfully.")
    except Exception as e:
        print(f"\nCould not connect to REAPER: {e}")

if __name__ == "__main__":
    create_scale_tutor()
