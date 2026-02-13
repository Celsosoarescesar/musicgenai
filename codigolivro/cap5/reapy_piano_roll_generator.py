import reapy

# List of General MIDI instruments for display
GM_INSTRUMENTS = [
    "Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano",
    "Electric Piano 1", "Electric Piano 2", "Harpsichord", "Clavi",
    "Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer",
    "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accordion", "Harmonica", "Tango Accordion",
    "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar", "Guitar harmonics",
    "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass", "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2",
    "Violin", "Viola", "Cello", "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani",
    "String Ensemble 1", "String Ensemble 2", "SynthStrings 1", "SynthStrings 2", "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit",
    "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section", "SynthBrass 1", "SynthBrass 2",
    "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", "Bassoon", "Clarinet",
    "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina",
    "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)", "Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)",
    "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)", "Pad 5 (bowed)", "Pad 6 (metallic)", "Pad 7 (halo)", "Pad 8 (sweep)",
    "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)", "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)",
    "Sitar", "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle", "Shanai",
    "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal",
    "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter", "Applause", "Gunshot"
]

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

def create_piano_roll_interactive():
    print("--- Interactive Piano Roll Generator ---")
    
    try:
        inst_idx = int(input("Select MIDI instrument (0-127): "))
        if inst_idx < 0 or inst_idx > 127: inst_idx = 0
    except ValueError:
        print("Invalid input. Defaulting to 0 (Acoustic Grand Piano).")
        inst_idx = 0
        
    print(f"You picked: {GM_INSTRUMENTS[inst_idx]}")
    
    try:
        how_many = int(input("How many notes to play (0 or more): "))
    except ValueError:
        how_many = 0
        
    pitches = []
    for i in range(how_many):
        pitch_str = input(f"Enter note {i+1} (e.g., C4): ")
        pitches.append(note_to_midi(pitch_str))
        
    if not pitches:
        print("No notes entered. Exiting.")
        return

    # REAPER Integration
    try:
        project = reapy.Project()
        track = project.add_track(name=f"User Piano Roll ({GM_INSTRUMENTS[inst_idx]})")
        
        # Add ReaSynth as a placeholder since GM instruments depend on the user's setup
        synth = track.add_fx("ReaSynth")
        
        tempo = project.bpm
        if not tempo or tempo == 0: tempo = 120.0
        spb = 60.0 / tempo
        
        # MIDI parameters
        duration = 1.0 # Quarter Note (QN)
        total_beats = len(pitches) * duration
        
        item = track.add_midi_item(0, end=total_beats * spb)
        item.name = f"User Notes ({GM_INSTRUMENTS[inst_idx]})"
        take = item.active_take
        
        # Add Program Change (if possible in reapy, otherwise just note velocity)
        # Note: reapy doesn't have a direct 'add_program_change' easily exposed in basic Take,
        # but we can at least place the notes. 
        # For actual GM playback, the user would need a GM soundfont player.
        
        for i, pitch in enumerate(pitches):
            take.add_note(
                pitch=int(pitch),
                start=float(i * duration * spb),
                end=float((i * duration + 0.9) * spb),
                velocity=100,
                channel=0
            )
            
        print(f"\nGenerated {len(pitches)} notes for '{GM_INSTRUMENTS[inst_idx]}' in REAPER.")
        
    except Exception as e:
        print(f"Error connecting to REAPER: {e}")

if __name__ == "__main__":
    create_piano_roll_interactive()
