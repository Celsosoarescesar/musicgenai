import reapy

def create_trias_harmonica():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo to 100 BPM
    project.set_info_value("tempo", 100.0)
    
    # Musical definitions
    # Theme 1 (for choir 1)
    p1 = [60, 62, 64, 65, 67, 65, 64, 62] # C4, D4, E4, F4, G4, F4, E4, D4
    # Theme 2 (inverted, for choir 2)
    p2 = [67, 65, 64, 62, 60, 62, 64, 65] # G4, F4, E4, D4, C4, D4, E4, F4
    
    # Durations (in beats)
    # DQN = 1.5 (Dotted Quarter Note), EN = 0.5 (Eighth Note)
    durations = [1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 0.5]
    
    times = 8 # Repeat 8 times
    spb = 60.0 / 100.0 # Seconds per beat at 100 BPM
    
    def insert_voice(track_name, pitch_list, initial_delay_beats, final_pitch):
        track = project.add_track(name=track_name)
        # Add ReaSynth
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = 0.0 # Fast attack
            synth.params[2] = 0.6 # Decay
            synth.params[3] = 0.0 # No sustain
            
        one_theme_duration_beats = sum(durations)
        total_duration_beats = initial_delay_beats + (one_theme_duration_beats * times) + 1.5 # + DQN for final note
        total_duration_seconds = total_duration_beats * spb
        
        # Create MIDI item
        # reapy item start/end are in project seconds
        item = track.add_midi_item(0, end=total_duration_seconds)
        item.name = track_name + " Take"
        take = item.active_take
        
        current_beat = initial_delay_beats
        
        for r in range(times):
            for pitch, dur in zip(pitch_list, durations):
                note_start = current_beat * spb
                note_end = (current_beat + dur * 0.9) * spb
                
                take.add_note(
                    pitch=int(pitch),
                    start=float(note_start),
                    end=float(note_end),
                    velocity=80,
                    channel=0
                )
                current_beat += dur
        
        # Add final note
        note_start = current_beat * spb
        note_end = (current_beat + 1.5 * 0.9) * spb
        take.add_note(pitch=int(final_pitch), start=float(note_start), end=float(note_end), velocity=80, channel=0)

    # Choir 1 - 4 voices separated by half note (2 beats)
    insert_voice("Choir 1 - Voice 1", p1, 0.0, 60) # C4
    insert_voice("Choir 1 - Voice 2", p1, 2.0, 60)
    insert_voice("Choir 1 - Voice 3", p1, 4.0, 60)
    insert_voice("Choir 1 - Voice 4", p1, 6.0, 60)
    
    # Choir 2 - 4 voices inverted, delayed by quarter note (1 beat), separated by half note (2 beats)
    insert_voice("Choir 2 - Voice 1", p2, 1.0, 67) # G4
    insert_voice("Choir 2 - Voice 2", p2, 3.0, 67)
    insert_voice("Choir 2 - Voice 3", p2, 5.0, 67)
    insert_voice("Choir 2 - Voice 4", p2, 7.0, 67)

    print("Bach Trias Harmonica canon generated successfully in REAPER.")

if __name__ == "__main__":
    try:
        create_trias_harmonica()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure REAPER is open and reapy is correctly configured.")
