import reapy
import random

def create_drums_come_alive():
    # Connect to REAPER
    project = reapy.Project()
    
    # 1. Musical Parameters
    tempo = 125.0
    project.bpm = tempo
    spb = 60.0 / tempo # Seconds per beat
    
    come_alive_prob = 0.35 # Probability of open hi-hat on odd hits
    measures = 8
    
    # MIDI Pitch Mappings for Drums (General MIDI standards)
    KICK = 35         # Acoustic Bass Drum
    SNARE = 38        # Acoustic Snare
    CLOSED_HH = 42    # Closed Hi Hat
    OPEN_HH = 46      # Open Hi Hat
    
    # Durations in beats
    HN = 2.0  # Half Note
    QN = 1.0  # Quarter Note
    SN = 0.25 # Sixteenth Note (1/16)
    
    all_notes = [] # List of (pitch, start_beat, duration, velocity)

    # 2. Generate Kick Pattern
    # One kick every 2 beats
    for i in range(2 * measures):
        start_beat = i * HN
        velocity = random.randint(80, 110)
        all_notes.append((KICK, start_beat, HN, velocity))

    # 3. Generate Snare Pattern
    # One rest (1 beat) + one snare (1 beat) repeated
    for i in range(2 * measures):
        # i*2 + 1 to account for the REST in the first beat of each 2-beat segment
        start_beat = i * 2.0 + 1.0 
        velocity = random.randint(80, 110)
        all_notes.append((SNARE, start_beat, QN, velocity))

    # 4. Generate Hi-Hat Pattern
    # A hi-hat pulse: hi-hat + rest (each 1/16 note)
    # 8 segments of (HH + REST) per measure = 16 hits total per measure
    for i in range(16 * measures):
        # Time position in beats
        start_beat = i * (SN * 2) # i * 0.5 beats (8 hits per measure)
        # Wait, the original script does (one hi-hat + one rest) x 8 = 1 measure?
        # That means 8 pulses per measure. Each pulse = SN (note) + SN (rest) = 0.5 beats.
        # Total per measure = 8 * 0.5 = 4 beats. Correct.
        
        # Check if it's an "odd hit" (indices 1, 3, 5...)
        is_odd_hit = i % 2 == 1
        
        # Stochastic choice for human-like variation
        if is_odd_hit and random.random() < come_alive_prob:
            pitch = OPEN_HH
        else:
            pitch = CLOSED_HH
            
        velocity = random.randint(80, 110)
        all_notes.append((pitch, start_beat, SN, velocity))

    # 5. REAPER Integration
    track = project.add_track(name="Drums Come Alive (Humanized)")
    # Using ReaSynth as a placeholder, but in REAPER channel 10/MIDI 9 
    # would usually be a drum VST like RS5K.
    synth = track.add_fx("ReaSynth")
    if synth:
        # Percussive setting for ReaSynth
        synth.params[1] = 0.001 # Attack
        synth.params[2] = 0.2   # Fast decay
        synth.params[3] = 0.0   # No sustain
        
    # Total duration is 8 measures * 4 beats/measure = 32 beats
    total_beats = measures * 4.0
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Stochastic Drum Pattern"
    take = item.active_take
    
    # Add all generated notes
    for pitch, start_beat, dur, vel in all_notes:
        take.add_note(
            pitch=int(pitch),
            start=float(start_beat * spb),
            end=float((start_beat + dur * 0.95) * spb), # Slightly shorter to avoid overlap
            velocity=int(vel),
            channel=9 # MIDI Channel 10 is index 9
        )

    print(f"Humanized drum pattern ({measures} measures) generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_drums_come_alive()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
