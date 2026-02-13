import reapy

def create_arpeggio():
    # Connect to REAPER
    project = reapy.Project()
    
    # Arpeggio parameters
    # C4, E4, G4, C5, G4, E4
    arpeggio_pattern = [60, 64, 67, 72, 67, 64]
    
    # TN (Thirty-second Note) duration in beats
    # Quarter Note (QN) = 1.0, TN = QN / 8 = 0.125
    duration = 0.125 
    
    try:
        user_input = input("How many times to repeat arpeggio: ")
        repetitions = int(user_input)
    except ValueError:
        print("Invalid input. Using default (2 repetitions).")
        repetitions = 2
    
    # REAPER Setup
    track = project.add_track(name="Arpeggiator")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.0 # Fast attack
        synth.params[2] = 0.4 # Short decay for arpeggio
        synth.params[3] = 0.0 # No sustain
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    # Calculate total length
    one_repeat_beats = len(arpeggio_pattern) * duration
    total_beats = (one_repeat_beats * repetitions) + (duration * 2) # Pattern + final long note
    
    # Create MIDI item
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Arpeggio Take"
    take = item.active_take
    
    current_beat = 0.0
    
    # Add repeated pattern
    for _ in range(repetitions):
        for pitch in arpeggio_pattern:
            take.add_note(
                pitch=int(pitch),
                start=float(current_beat * spb),
                end=float((current_beat + duration * 0.9) * spb),
                velocity=100,
                channel=0
            )
            current_beat += duration
            
    # Add final note (first pitch, longer duration)
    last_pitch = arpeggio_pattern[0]
    final_duration = duration * 2
    take.add_note(
        pitch=int(last_pitch),
        start=float(current_beat * spb),
        end=float((current_beat + final_duration * 0.9) * spb),
        velocity=100,
        channel=0
    )

    print(f"Arpeggiator generated in REAPER with {repetitions} repetitions.")

if __name__ == "__main__":
    try:
        create_arpeggio()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
