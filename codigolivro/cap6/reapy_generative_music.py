import reapy
import random

def create_generative_music():
    # Connect to REAPER
    project = reapy.Project()
    
    num_notes = 32 # how many random notes to play
    
    # Pitches: C4, D4, E4, F4, G4, A4, B4, C5
    pitches = [60, 62, 64, 65, 67, 69, 71, 72]
    # Durations in beats: QN=1.0, EN=0.5, SN=0.25
    QN, EN, SN = 1.0, 0.5, 0.25
    durations = [QN, EN, QN, EN, QN, EN, SN, QN]
    # Weights for each pitch/duration pair
    chances = [5, 1, 3, 2, 4, 3, 1, 5]
    
    # Create weighted lists
    weighted_pitches = []
    weighted_durs = []
    for i in range(len(chances)):
        weighted_pitches.extend([pitches[i]] * chances[i])
        weighted_durs.extend([durations[i]] * chances[i])
        
    # Generate the sequence
    melody = []
    for _ in range(num_notes):
        idx = random.randint(0, len(weighted_pitches) - 1)
        melody.append((weighted_pitches[idx], weighted_durs[idx]))
        
    # REAPER Integration
    track = project.add_track(name="Generative Music (Weighted Probabilities)")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.01 # Plucky attack
        synth.params[2] = 0.5  # Medium decay
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    total_beats = sum(n[1] for n in melody)
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Stochastic Weighted Sequence"
    take = item.active_take
    
    current_beat = 0.0
    for pitch, dur in melody:
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + dur * 0.9) * spb),
            velocity=random.randint(90, 110),
            channel=0
        )
        current_beat += dur

    print(f"Weighted generative sequence with {num_notes} notes generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_generative_music()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
