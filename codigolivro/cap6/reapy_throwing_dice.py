import reapy
import random

def create_throwing_dice_melody():
    # Connect to REAPER
    project = reapy.Project()
    
    num_notes = 14 # how many random notes to play
    
    # Dice to Pitch Mapping
    # 1: C4, 2: D4, 3: E4, 4: F4, 5: G4, 6: A4
    dice_map = {
        1: 60, # C4
        2: 62, # D4
        3: 64, # E4
        4: 65, # F4
        5: 67, # G4
        6: 69  # A4
    }
    
    # Generate the melody based on dice rolls
    melody = []
    for i in range(num_notes):
        dice = random.randint(1, 6) # throw dice
        pitch = dice_map.get(dice)
        melody.append(pitch)
        
    # REAPER Integration
    track = project.add_track(name="Throwing Dice Melody")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.01 # Fast attack
        synth.params[2] = 0.6  # Medium decay
        
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    duration_beats = 1.0 # QN
    total_beats = num_notes * duration_beats
    
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Stochastic Dice Melody"
    take = item.active_take
    
    current_beat = 0.0
    for pitch in melody:
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + duration_beats * 0.9) * spb),
            velocity=random.randint(90, 110),
            channel=0
        )
        current_beat += duration_beats

    print(f"Throwing Dice melody with {num_notes} notes generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_throwing_dice_melody()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
