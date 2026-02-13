import reapy
import random

def map_value(val, in_min, in_max, out_min, out_max):
    """Linearly maps a value from one range to another (clamped to output range)."""
    if in_max == in_min:
        return out_min
    result = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(int(out_min), min(int(out_max), int(result)))

def get_pentatonic_pitch(index):
    """Maps an index to a MIDI pitch in C Pentatonic scale (C3 = index 0)."""
    # C Pentatonic: C, D, E, G, A (0, 2, 4, 7, 9)
    scale_degrees = [0, 2, 4, 7, 9]
    octave = index // 5
    degree = index % 5
    return (octave * 12) + scale_degrees[degree] + 48 # Start at C3

def create_text_music():
    # Connect to REAPER
    project = reapy.Project()
    
    # 1. Text to sonify (Moby-Dick Epilogue)
    text = "The drama's done. Why then here does any one step forth? - Because one did survive the wreck. "
    
    # Durations mapping (weighted)
    # HN=2.0, QN=1.0, EN=0.5, SN=0.25
    HN, QN, EN, SN = 2.0, 1.0, 0.5, 0.25
    durations_list = [HN] + [QN]*4 + [EN]*4 + [SN]*2
    
    # Settings
    project.bpm = 130.0
    spb = 60.0 / 130.0
    
    all_notes = [] # List of (pitch, start_beat, duration, velocity)
    current_beat = 0.0
    
    print(f"Sonifying {len(text)} characters...")
    
    last_pitch = 60 # Default
    
    for char in text:
        val = ord(char) # ASCII value
        
        # ASCII printable range is 32 to 126
        # Map to Pentatonic scale index (let's say 20 notes range C3 to C7 approx)
        pitch_idx = map_value(val, 32, 126, 0, 19)
        pitch = get_pentatonic_pitch(pitch_idx)
        last_pitch = pitch
        
        # Map to durations list index
        dur_idx = map_value(val, 32, 126, 0, len(durations_list) - 1)
        duration = durations_list[dur_idx]
        
        velocity = random.randint(60, 120)
        
        all_notes.append((pitch, current_beat, duration, velocity))
        current_beat += duration
        
    # Add final long note (WN = 4.0 beats)
    all_notes.append((last_pitch, current_beat, 4.0, 100))
    current_beat += 4.0

    # 2. REAPER Integration
    track = project.add_track(name="Text Music (Moby-Dick)")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Delicate mallet/glockenspiel sound
        synth.params[1] = 0.001 # Attack
        synth.params[2] = 0.4   # Decay
        
    item = track.add_midi_item(0, end=current_beat * spb)
    item.name = "Literature Sonification"
    take = item.active_take
    
    for pitch, start_beat, dur, vel in all_notes:
        take.add_note(
            pitch=int(pitch),
            start=float(start_beat * spb),
            end=float((start_beat + dur * 0.9) * spb),
            velocity=int(vel),
            channel=0
        )

    print("Text Music (Moby-Dick) generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_text_music()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
