import reapy
import random

def create_mozart_dice_game():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo (suitable for a waltz)
    tempo = 120.0
    project.bpm = tempo
    spb = 60.0 / tempo # Seconds per beat

    # MIDI Pitch Mappings
    C2, G2, B2 = 36, 43, 47
    C3, E3, G3 = 48, 52, 55
    C4, E4, G4, A4, B4 = 60, 64, 67, 69, 71
    C5, D5, E5, F5 = 72, 74, 76, 77
    CS3 = 49 # C#3
    
    # Durations in beats (3/8 time signature context)
    # QN=1.0, EN=0.5, SN=0.25, DQN=1.5
    QN, EN, SN, DQN = 1.0, 0.5, 0.25, 1.5

    # Measure alternatives (Choices from the matrix)
    
    # Measure 1 alternatives
    m1_choices = [
        # Choice 96
        {"p": [[C3, E5], C5, G4], "d": [EN, EN, EN]},
        # Choice 32
        {"p": [[C3, E3, G4], C5, E5], "d": [EN, EN, EN]},
        # Choice 40
        {"p": [[C3, E3, C5], B4, C5, E5, G4, C5], "d": [SN, SN, SN, SN, SN, SN]}
    ]
    
    # Measure 2 alternatives
    m2_choices = [
        # Choice 6 (same as choice 32)
        {"p": [[C3, E3, G4], C5, E5], "d": [EN, EN, EN]},
        # Choice 17
        {"p": [[E3, G3, C5], G4, C5, E5, G4, C5], "d": [SN, SN, SN, SN, SN, SN]}
    ]
    
    # Measure 3 alternatives
    m3_choices = [
        # Choice 141
        {"p": [[B2, G3, D5], E5, F5, D5, [G2, C5], B4], "d": [SN, SN, SN, SN, SN, SN]},
        # Choice 158
        {"p": [[G2, B4], D5, B4, A4, G4], "d": [EN, SN, SN, SN, SN]}
    ]
    
    # Measure 4 alternatives
    m4_choices = [
        # Choice 30
        {"p": [[C5, G4, E4, C4, C2]], "d": [DQN]},
        # Choice 5
        {"p": [[C2, C5, G4, E4, C4], [G2, B4], [C2, E4, C5]], "d": [SN, SN, QN]}
    ]

    # Roll the dice!!!
    selected_measures = [
        random.choice(m1_choices),
        random.choice(m2_choices),
        random.choice(m3_choices),
        random.choice(m4_choices)
    ]

    # 2. REAPER Integration
    track = project.add_track(name="Mozart Dice Game (Waltz)")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.01 # Plucky attack
        synth.params[2] = 0.8  # Longer decay for piano-like feel
        
    # Each measure has 1.5 beats (3/8 time)
    total_beats = 4 * 1.5 
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Stochastic Waltz"
    take = item.active_take
    
    current_beat = 0.0
    for measure in selected_measures:
        for p_chord, dur in zip(measure["p"], measure["d"]):
            # Handle both single notes and chord lists
            pitches = p_chord if isinstance(p_chord, list) else [p_chord]
            for pitch in pitches:
                take.add_note(
                    pitch=int(pitch),
                    start=float(current_beat * spb),
                    end=float((current_beat + dur * 0.9) * spb),
                    velocity=random.randint(90, 110), # Slight humanization
                    channel=0
                )
            current_beat += dur

    print("Mozart's Dice Game excerpt generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_mozart_dice_game()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
