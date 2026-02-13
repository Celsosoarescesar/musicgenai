import reapy

def create_general_retrograde():
    # Connect to REAPER
    project = reapy.Project()
    
    # 1. Setup Source Track with some initial notes
    source_track = project.add_track(name="Source (Original)")
    source_track.add_fx("ReaSynth")
    
    # Define a sequence: C4 (1.0s), E4 (0.5s), G4 (0.5s), C5 (2.0s)
    source_pitches = [60, 64, 67, 72]
    source_durations = [1.0, 0.5, 0.5, 2.0]
    
    total_source_len = sum(source_durations)
    item = source_track.add_midi_item(0, end=total_source_len)
    take = item.active_take
    
    cursor = 0.0
    for p, d in zip(source_pitches, source_durations):
        take.add_note(pitch=p, start=cursor, end=cursor + d * 0.9, velocity=100)
        cursor += d
        
    print("Source track created with a C major chord progression.")
    
    # 2. Extract and Retrograde
    # In a real-world scenario, you might get 'take' from a selected item:
    # take = reapy.Project().selected_items[0].active_take
    
    notes_data = []
    for note in take.notes:
        pitch = note.pitch
        duration = note.end - note.start
        notes_data.append((pitch, duration))
        
    # Reverse the sequence
    notes_data.reverse()
    
    # 3. Create Retrograde Track
    retro_track = project.add_track(name="General Retrograde (Reversed)")
    retro_track.add_fx("ReaSynth")
    
    total_retro_len = sum(d for p, d in notes_data)
    # Start after source finishes + 2s gap
    start_time = total_source_len + 2.0
    
    retro_item = retro_track.add_midi_item(start_time, end=start_time + total_retro_len)
    retro_take = retro_item.active_take
    
    cursor = 0.0
    for p, d in notes_data:
        # Note: the original durations are preserved, but played in reverse order
        retro_take.add_note(pitch=int(p), start=cursor, end=cursor + d, velocity=100)
        cursor += d

    print("General retrograde track created in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_general_retrograde()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
