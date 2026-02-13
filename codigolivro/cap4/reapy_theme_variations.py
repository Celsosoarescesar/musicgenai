import reapy
import random

def create_theme_variations():
    # Connect to REAPER
    project = reapy.Project()
    project.set_info_value("tempo", 120.0) # Default tempo
    
    # Helper functions for transformations
    def randomize(notes, amount):
        return [(p + random.randint(-amount, amount), d) for p, d in notes]

    def mutate(notes, count=1):
        new_notes = list(notes)
        for _ in range(count):
            idx = random.randint(0, len(new_notes) - 1)
            p, d = new_notes[idx]
            # Mutate pitch or rhythm
            if random.random() > 0.5:
                p += random.choice([-2, -1, 1, 2])
            else:
                d *= random.choice([0.5, 2.0])
            new_notes[idx] = (p, d)
        return new_notes

    def elongate(notes, factor):
        return [(p, d * factor) for p, d in notes]

    def retrograde(notes):
        return list(reversed(notes))

    def transpose(notes, interval):
        return [(p + interval, d) for p, d in notes]

    def quantize(notes, grid=0.25, scale=[0, 2, 4, 5, 7, 9, 11]):
        quantized = []
        for p, d in notes:
            # Quantize rhythm
            new_d = round(d / grid) * grid
            if new_d == 0: new_d = grid
            
            # Quantize pitch to scale
            octave = (p // 12) * 12
            degree = p % 12
            # Find nearest scale degree
            nearest_degree = min(scale, key=lambda x: abs(x - degree))
            new_p = octave + nearest_degree
            
            quantized.append((new_p, new_d))
        return quantized

    # Original Theme
    # Pitches: C4, E4, G4, A4, B4, A4, B4, C5
    # Durations: EN, EN, QN, SN, SN, SN, SN, QN (0.5, 0.5, 1.0, 0.25...)
    theme = [
        (60, 0.5), (64, 0.5), (67, 1.0), (69, 0.25), 
        (71, 0.25), (69, 0.25), (71, 0.25), (72, 1.0)
    ]
    
    # Var 1: Randomize
    var1 = randomize(theme, 3)
    
    # Var 2: Elongate and Mutate
    var2 = elongate(theme, 2.0)
    var2 = mutate(var2, 2)
    
    # Var 3: Retrograde and Transpose
    var3 = retrograde(theme)
    var3 = transpose(var3, -12)
    
    # Var 4: Recapitulation
    var4 = list(theme)
    
    # Combine and Quantize the whole part
    all_sections = theme + var1 + var2 + var3 + var4
    final_notes = quantize(all_sections)
    
    # REAPER Integration
    track = project.add_track(name="Theme & Variations")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.0 # Fast attack
        synth.params[2] = 0.6 # Decay
    
    spb = 60.0 / 120.0 # Seconds per beat
    total_beats = sum(d for p, d in final_notes)
    
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = "Variations Take"
    take = item.active_take
    
    current_beat = 0.0
    for p, d in final_notes:
        take.add_note(
            pitch=int(p),
            start=float(current_beat * spb),
            end=float((current_beat + d * 0.9) * spb),
            velocity=100,
            channel=0
        )
        current_beat += d

    print("Theme and Variations generated successfully in REAPER (Quantized to C Major).")

if __name__ == "__main__":
    try:
        create_theme_variations()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
