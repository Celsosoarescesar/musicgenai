import reapy

def create_retrograde_demo():
    # Connect to REAPER
    project = reapy.Project()
    
    # Musical Parameters
    # C major scale: C4, D4, E4, F4, G4, A4, B4, C5
    pitches = [60, 62, 64, 65, 67, 69, 71, 72]
    # Rhythms: WN, HN, QN, EN, SN, TN, TN/2, TN/4 (decreasing durations = increasing tempo)
    rhythms = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
    
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat

    def insert_notes(track_name, p_list, r_list, start_offset_beats=0):
        track = project.add_track(name=track_name)
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = 0.01 # Almost instant attack
            synth.params[2] = 0.5 # Medium decay
            
        total_beats = sum(r_list)
        start_seconds = start_offset_beats * spb
        
        item = track.add_midi_item(start_seconds, end=start_seconds + total_beats * spb)
        item.name = f"{track_name} Take"
        take = item.active_take
        
        current_beat = 0.0
        for p, r in zip(p_list, r_list):
            take.add_note(
                pitch=int(p),
                start=float(current_beat * spb),
                end=float((current_beat + r * 0.9) * spb),
                velocity=100,
                channel=0
            )
            current_beat += r

    # 1. Original: C major scale, accelerating
    insert_notes("Original (Accelerating Up)", pitches, rhythms)
    
    # 2. Retrograde: Reversed pitches and reversed rhythms
    # Reverse the lists for retrograde
    rev_pitches = list(reversed(pitches))
    rev_rhythms = list(reversed(rhythms))
    
    # Start the retrograde after the original finishes (plus a bit of space)
    original_duration_beats = sum(rhythms)
    insert_notes("Retrograde (Decelerating Down)", rev_pitches, rev_rhythms, start_offset_beats=original_duration_beats + 2)

    print("Retrograde demonstration generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_retrograde_demo()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
