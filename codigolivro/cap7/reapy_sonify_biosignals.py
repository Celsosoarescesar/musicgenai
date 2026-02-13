import reapy
import os

def map_value(val, in_min, in_max, out_min, out_max):
    """Linearly maps a value from one range to another."""
    if in_max == in_min:
        return out_min
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def quantize_to_c_major(pitch):
    """Quantizes a MIDI pitch to the nearest note in the C Major scale."""
    c_major_intervals = [0, 2, 4, 5, 7, 9, 11]
    octave = pitch // 12
    note_in_octave = pitch % 12
    closest_note = min(c_major_intervals, key=lambda x: abs(x - note_in_octave))
    return (octave * 12) + closest_note

def create_biosignal_sonification():
    # Connect to REAPER
    project = reapy.Project()
    
    # Path to the data file
    data_file = os.path.join(os.path.dirname(__file__), "biosignals.txt")
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Please run the dummy data creation first.")
        return

    # 1. Read and process data
    skin_data = []
    heart_data = []
    
    with open(data_file, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                # time = float(parts[0])
                # parts[1] is skin conductance, parts[2] is heart rate
                skin_data.append(float(parts[1]))
                heart_data.append(float(parts[2]))

    if not skin_data:
        print("Error: No data found in biosignals.txt")
        return

    # Find ranges for mapping
    skin_min, skin_max = min(skin_data), max(skin_data)
    heart_min, heart_max = min(heart_data), max(heart_data)

    # 2. REAPER Integration
    track = project.add_track(name="Biosignal Sonification")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Piano-like setting
        synth.params[1] = 0.001 # Attack
        synth.params[2] = 0.5   # Decay
        synth.params[3] = 0.1   # Sustain

    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 150.0
    spb = 60.0 / tempo # Seconds per beat
    
    # 32nd note duration (TN)
    # 1 beat = QN, 0.5 = EN, 0.25 = SN, 0.125 = TN
    dur_beats = 0.125 
    
    total_beats = len(heart_data) * dur_beats
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Biological Data Melody"
    take = item.active_take
    
    current_beat = 0.0
    for i in range(len(heart_data)):
        # Map skin conductance to base pitch (C3=48 to C6=84)
        base_pitch = map_value(skin_data[i], skin_min, skin_max, 48, 84)
        
        # Map heart data to pitch variation (0 to 24 semitones)
        variation = map_value(heart_data[i], heart_min, heart_max, 0, 24)
        
        # Resulting pitch
        raw_pitch = base_pitch + variation
        
        # Quantize to C Major
        pitch = quantize_to_c_major(int(raw_pitch))
        
        # Map heart data to velocity (0-127)
        velocity = map_value(heart_data[i], heart_min, heart_max, 60, 110) # Using a narrower range for better sound
        
        take.add_note(
            pitch=int(pitch),
            start=float(current_beat * spb),
            end=float((current_beat + dur_beats * 0.9) * spb),
            velocity=int(velocity),
            channel=0
        )
        current_beat += dur_beats

    print(f"Biosignal sonification with {len(heart_data)} data points generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_biosignal_sonification()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
