import reapy

def create_bach_canon():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo to 100 BPM
    project.set_info_value("tempo", 100.0)
    
    # Musical definitions
    # Goldberg Ground Subject (Soggetto)
    # G3, F3, E3, D3, B2, C3, D3, G2
    # MIDI: 55, 53, 52, 50, 47, 48, 50, 43
    pitches = [55, 53, 52, 50, 47, 48, 50, 43]
    durations = [1.0] * 8  # All Quarter Notes (QN)
    
    times = 6  # Repeat 6 times
    spb = 60.0 / 100.0 # Seconds per beat at 100 BPM
    
    def insert_voice(track_name, pitch_list, repeats):
        track = project.add_track(name=track_name)
        # Add ReaSynth
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = 0.0 # Fast attack
            synth.params[2] = 0.6 # Decay
            synth.params[3] = 0.0 # No sustain
            
        total_duration_beats = len(pitch_list) * repeats
        total_duration_seconds = total_duration_beats * spb
        
        # Create MIDI item
        item = track.add_midi_item(0, total_duration_seconds)
        item.name = track_name + " Take"
        take = item.active_take
        
        current_beat = 0.0
        for r in range(repeats):
            for pitch in pitch_list:
                note_start = current_beat * spb
                note_end = (current_beat + 0.9) * spb # 0.9 for slight articulation gap
                
                take.add_note(
                    pitch=int(pitch),
                    start=float(note_start),
                    end=float(note_end),
                    velocity=90,
                    channel=0
                )
                current_beat += 1.0 # 1 beat per note

    # Voice 1: Original subject
    insert_voice("Voice 1 (Leader)", pitches, times)
    
    # Voice 2: Retrograde (reverse) of the subject
    retro_pitches = list(reversed(pitches))
    insert_voice("Voice 2 (Retrograde Follower)", retro_pitches, times)

    print("Bach Goldberg Canon generated successfully in REAPER.")

if __name__ == "__main__":
    try:
        create_bach_canon()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure REAPER is open and reapy is correctly configured.")
