import reapy

def create_economical_retrograde():
    # Connect to REAPER
    project = reapy.Project()
    
    # 1. Setup Source Track
    source_track = project.add_track(name="Source (for Economical Intro)")
    source_track.add_fx("ReaSynth")
    
    # A simple melodic phrase: E4, G4, A4, B4 with different lengths
    source_pitches = [64, 67, 69, 71]
    source_durations = [0.5, 0.5, 1.0, 2.0] # in seconds
    
    total_source_len = sum(source_durations)
    item = source_track.add_midi_item(0, end=total_source_len)
    take = item.active_take
    
    cursor = 0.0
    for p, d in zip(source_pitches, source_durations):
        take.add_note(pitch=p, start=cursor, end=cursor + d * 0.9, velocity=90)
        cursor += d
        
    print("Source track created with a simple 4-note melody.")
    
    # 2. Extract notes into a list
    note_list = list(take.notes)
    num_notes = len(note_list)
    
    pitches = []
    durations = []
    
    # 3. Iterate BACKWARDS manually
    print(f"Processing {num_notes} notes in reverse order...")
    for i in range(num_notes):
        # Calculate index from the other end of the list
        reverse_index = num_notes - i - 1
        
        note = note_list[reverse_index]
        
        pitches.append(note.pitch)
        durations.append(note.end - note.start)
        
    # 4. Create Retrograde Track
    retro_track = project.add_track(name="Retrograde (Economical Loop)")
    retro_track.add_fx("ReaSynth")
    
    total_retro_len = sum(durations)
    # Start after source finishes + 2s gap
    start_time = total_source_len + 2.0
    
    retro_item = retro_track.add_midi_item(start_time, end=start_time + total_retro_len)
    retro_take = retro_item.active_take
    
    cursor = 0.0
    for p, d in zip(pitches, durations):
        retro_take.add_note(pitch=int(p), start=cursor, end=cursor + d, velocity=100)
        cursor += d

    print("Economical retrograde track generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_economical_retrograde()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
