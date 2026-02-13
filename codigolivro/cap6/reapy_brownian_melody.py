import reapy
import random

def get_major_scale_pitch(index):
    """Maps a scale index to a MIDI pitch in C Major, where 0 is C4."""
    scale_degrees = [0, 2, 4, 5, 7, 9, 11]
    octave = index // 7
    degree = index % 7
    return (octave * 12) + scale_degrees[degree] + 60

def create_brownian_melody():
    # Connect to REAPER
    project = reapy.Project()
    
    # Set tempo to 130 BPM
    tempo = 130.0
    project.bpm = tempo
    spb = 60.0 / tempo # Seconds per beat
    
    number_of_notes = 30 # 1 initial + 29 generated
    duration_beats = 0.5 # EN (Eighth Note)
    
    indices = []
    current_index = 0 # Start at C4
    indices.append(current_index)
    
    for _ in range(number_of_notes - 1):
        # Flip a coin: 50% chance to go up or down 1 scale degree
        if random.random() < 0.5:
            current_index += 1
        else:
            current_index -= 1
        indices.append(current_index)
        
    pitches = [get_major_scale_pitch(idx) for idx in indices]
    
    # REAPER Integration
    track = project.add_track(name="Brownian Melody (Random Walk)")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Tuning for a Bell-like sound (Tubular Bells style)
        synth.params[1] = 0.005 # Attack
        synth.params[2] = 0.8   # Decay
        synth.params[3] = 0.0   # Sustain
        
    total_beats = number_of_notes * duration_beats
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Brownian Motion Sequence"
    take = item.active_take
    
    current_beat = 0.0
    for pitch in pitches:
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + duration_beats * 0.9) * spb),
            velocity=random.randint(90, 110),
            channel=0
        )
        current_beat += duration_beats

    print(f"Brownian melody with {number_of_notes} notes generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_brownian_melody()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
