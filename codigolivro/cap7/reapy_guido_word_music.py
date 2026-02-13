import reapy

def create_guido_word_music():
    # Connect to REAPER
    project = reapy.Project()
    
    # This is the text to be sonified
    text = "One of the oldest known algorithmic music processes is a rule-based algorithm that selects each note based on the letters in a text, credited to Guido d'Arezzo."
    text = text.lower()
    
    # Define vowels and corresponding pitches
    vowel_map = {
        'a': 60, # C4
        'e': 62, # D4
        'i': 64, # E4
        'o': 67, # G4
        'u': 69  # A4
    }
    
    # Factor used to scale durations
    duration_factor = 0.1 # higher for longer durations
    
    # Process text into pitches and durations
    pitches = []
    durations = []
    
    words = text.split()
    for word in words:
        # Clean word of punctuation for duration calculation if desired, 
        # but original uses raw word length
        word_len = len(word)
        
        for char in word:
            if char in vowel_map:
                pitches.append(vowel_map[char])
                durations.append(word_len * duration_factor)
                
    # REAPER Integration
    track = project.add_track(name="Guido Word Music (Vowels)")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Classic synth sound
        synth.params[1] = 0.01 # Attack
        synth.params[2] = 0.4  # Decay
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    total_beats = sum(durations)
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Stochastic Vowel Melody"
    take = item.active_take
    
    current_beat = 0.0
    for pitch, dur in zip(pitches, durations):
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + dur * 0.9) * spb),
            velocity=100,
            channel=0
        )
        current_beat += dur

    print(f"Guido Word Music generated with {len(pitches)} notes (vowels) in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_guido_word_music()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
