import reapy
import time

def create_row_your_boat():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo (108 BPM)
    # Using REAPER's master tempo
    project.set_info_value("tempo", 108.0)
    
    # Musical definitions
    # Pitches
    C4, D4, E4, F4, G4 = 60, 62, 64, 65, 67
    C5 = 72
    
    # Durations (in quarter notes/beats)
    QN = 1.0     # Quarter Note
    DEN = 0.75   # Dotted Eighth Note
    SN = 0.25    # Sixteenth Note
    HN = 2.0     # Half Note
    ENT = 1.0/3  # Eighth Note Triplet
    
    # Row, row, row your boat gently down the stream
    p1 = [C4, C4, C4, D4, E4, E4, D4, E4, F4, G4]
    d1 = [QN, QN, DEN, SN, QN, DEN, SN, DEN, SN, HN]
    
    # merrily, merrily, merrily, merrily
    p2 = [C5, C5, C5, G4, G4, G4, E4, E4, E4, C4, C4, C4]
    d2 = [ENT] * 12
    
    # life is but a dream.
    p3 = [G4, F4, E4, D4, C4]
    d3 = [DEN, SN, DEN, SN, HN]
    
    # Combine into a full theme
    theme_pitches = p1 + p2 + p3
    theme_durations = d1 + d2 + d3
    
    def insert_canon_part(track_name, start_beat, transposition, repeats=2):
        track = project.add_track(name=track_name)
        # Add a synth so we can hear it
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = 0.0 # Fast attack
            synth.params[2] = 0.5 # Decay
            synth.params[3] = 0.0 # No sustain
            
        # Calculate total duration in beats
        one_theme_duration = sum(theme_durations)
        total_duration = one_theme_duration * repeats
        
        # Convert beats to seconds for reapy (at 108 BPM)
        spb = 60.0 / 108.0
        start_seconds = start_beat * spb
        duration_seconds = total_duration * spb
        
        # Create MIDI item
        item = track.add_midi_item(start_seconds, duration_seconds)
        item.name = track_name + " Take"
        take = item.active_take
        
        current_beat = 0.0
        for r in range(repeats):
            for pitch, dur in zip(theme_pitches, theme_durations):
                # Calculate start/end in project seconds (relative to item start)
                # reapy add_note uses seconds relative to item start
                note_start = current_beat * spb
                note_end = (current_beat + dur * 0.9) * spb
                
                take.add_note(
                    pitch=int(pitch + transposition),
                    start=float(note_start),
                    end=float(note_end),
                    velocity=100,
                    channel=0
                )
                current_beat += dur
                
    # Create the three parts of the canon
    # Flute: Theme x 2, Transposed +12 (1 octave up), start at 0
    insert_canon_part("Flute Part", 0.0, 12)
    
    # Trumpet: Theme x 2, start at beat 4 (1 measure in 4/4)
    insert_canon_part("Trumpet Part", 4.0, 0)
    
    # Clarinet: Theme x 2, Transposed -12 (1 octave down), start at beat 8 (2 measures in 4/4)
    insert_canon_part("Clarinet Part", 8.0, -12)

    print("Row Your Boat canon generated successfully in REAPER.")

if __name__ == "__main__":
    try:
        create_row_your_boat()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure REAPER is open and reapy is correctly configured.")
