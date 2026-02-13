import reapy

def create_protein_music():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo to 220 BPM
    tempo = 220.0
    project.bpm = tempo
    spb = 60.0 / tempo # Seconds per beat
    
    # Pitches/Rhythms data (ThyA protein)
    # Pitches are lists of MIDI numbers representing chords
    pitches = [
        [50, 53, 57], [52, 55, 59], [59, 62, 65], [62, 65, 71],
        [62, 65, 69], [67, 71, 76], [67, 71, 74], [69, 48, 52],
        [59, 55, 52], [69, 72, 76], [69, 72, 76], [52, 55, 59],
        [57, 48, 52]
    ]
    # Rhythms in beats: HN=2.0, QN=1.0, EN=0.5, WN=4.0
    rhythms = [2.0, 1.0, 2.0, 1.0, 2.0, 0.5, 4.0, 4.0, 0.5, 1.0, 1.0, 1.0, 1.0]
    
    gap_beats = 2.0 # HN Silence gap
    
    # 1. Build the unfolding sequence
    # This list will store tuples of (pitch_list, duration, start_beat)
    full_sequence = []
    current_beat = 0.0
    
    for i in range(len(pitches)):
        # Get the slice for this iteration
        growing_pitches = pitches[:i+1]
        growing_rhythms = rhythms[:i+1]
        
        # Add the notes for this growing segment
        for p_chord, dur in zip(growing_pitches, growing_rhythms):
            full_sequence.append((p_chord, dur, current_beat))
            current_beat += dur
            
        # Add silence gap
        current_beat += gap_beats

    # 2. REAPER Integration
    track = project.add_track(name="Protein Music (ThyA)")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.01 # Fast attack
        synth.params[2] = 0.6  # Medium decay
        
    total_beats = current_beat
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Unfolding Protein Sequence"
    take = item.active_take
    
    for p_chord, dur, start_beat in full_sequence:
        for pitch in p_chord:
            take.add_note(
                pitch=int(pitch),
                start=float(start_beat * spb),
                end=float((start_beat + dur * 0.9) * spb),
                velocity=90,
                channel=0
            )

    print("Protein Music (unfolding piece) generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_protein_music()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
