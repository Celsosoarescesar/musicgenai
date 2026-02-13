import reapy

def create_arvo_part_cantus():
    # Connect to REAPER
    project = reapy.Project()
    
    # Musical parameters
    repetitions = 2   # piece length multiplier
    tempo = 112       # 112 bpm
    project.set_info_value("tempo", float(tempo))
    
    bar_beats = 6.0   # WN + HN (4 + 2)
    spb = 60.0 / tempo # Seconds per beat
    
    # Bell data
    # A4 (69)
    bell_pitches = [None, 69, None, None, 69, None, None, 69]
    bell_durations = [bar_beats/2.0, bar_beats/2.0, bar_beats, bar_beats/2.0, bar_beats/2.0, bar_beats, bar_beats/2.0, bar_beats/2.0]
    
    # Violin basic theme (Descending Aeolian)
    # A5, G5, F5, E5, D5, C5, B4, A4
    pitches = [81, 79, 77, 76, 74, 72, 71, 69]
    durations = [2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0] # HN, QN...
    
    # Create tracks and instruments
    def setup_track(name):
        track = project.add_track(name=name)
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = 0.0 # Fast attack
            synth.params[2] = 0.8 # Long decay for strings/bells
            synth.params[3] = 0.1 # Some sustain
        return track

    # Bell Part
    bell_track = setup_track("Tubular Bells")
    
    # Bell MIDI
    total_bell_beats = sum(bell_durations)
    bell_item = bell_track.add_midi_item(0, end=total_bell_beats * spb)
    bell_take = bell_item.active_take
    current_beat = 0.0
    for p, d in zip(bell_pitches, bell_durations):
        if p is not None:
            bell_take.add_note(pitch=int(p), start=current_beat * spb, end=(current_beat + d * 0.9) * spb, velocity=100, channel=0)
        current_beat += d

    # Violin Part
    def insert_violin_prolation(track_name, start_bar, transposition, elongation, reps):
        track = setup_track(track_name)
        
        # Calculate elongated theme
        long_pitches = pitches
        long_durations = [d * elongation for d in durations]
        theme_len_beats = sum(long_durations)
        total_beats = theme_len_beats * reps
        
        start_seconds = start_bar * bar_beats * spb
        duration_seconds = total_beats * spb
        
        item = track.add_midi_item(start_seconds, end=start_seconds + duration_seconds)
        item.name = track_name + " Take"
        take = item.active_take
        
        current_rel_beat = 0.0
        
        # Fade parameters (simplified with velocity ramping)
        total_notes = len(long_pitches) * reps
        
        for r in range(reps):
            for i, (p, d) in enumerate(zip(long_pitches, long_durations)):
                # Calculate velocity for fade-in/out
                note_index = r * len(long_pitches) + i
                # Simple ramp up and down
                if note_index < total_notes / 4: # Fade in
                    vel = int(40 + (note_index / (total_notes / 4)) * 60)
                elif note_index > (3 * total_notes / 4): # Fade out
                    vel = int(100 - ((note_index - 3 * total_notes / 4) / (total_notes / 4)) * 80)
                else:
                    vel = 100
                
                take.add_note(
                    pitch=int(p + transposition),
                    start=float(current_rel_beat * spb),
                    end=float((current_rel_beat + d * 0.9) * spb),
                    velocity=max(20, min(127, vel)),
                    channel=0
                )
                current_rel_beat += d
                
    # Prolation Canon Voices
    # Violin 1: 1x, start 6.5 bars, octave 0
    insert_violin_prolation("Violin 1", 6.5, 0, 1.0, 8 * repetitions)
    # Violin 2: 2x, start 7.0 bars, octave -1
    insert_violin_prolation("Violin 2", 7.0, -12, 2.0, 4 * repetitions)
    # Violin 3: 4x, start 8.0 bars, octave -2
    insert_violin_prolation("Violin 3", 8.0, -24, 4.0, 2 * repetitions)
    # Violin 4: 8x, start 10.0 bars, octave -3
    insert_violin_prolation("Violin 4", 10.0, -36, 8.0, 1 * repetitions)

    print("Arvo Part - Cantus in Memoriam Benjamin Britten generated in REAPER.")

if __name__ == "__main__":
    try:
        create_arvo_part_cantus()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
