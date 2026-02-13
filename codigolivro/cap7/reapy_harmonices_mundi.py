import reapy

def map_scale(val, in_min, in_max, out_min, out_max):
    """Linearly maps a value from one range to another."""
    if in_max == in_min:
        return out_min
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def create_celestial_canon():
    # Connect to REAPER
    project = reapy.Project()
    
    # 1. Planetary Data (Mean Orbital Velocities in km/s)
    # Mercury, Venus, Earth, Mars, Ceres, Jupiter, Saturn, Uranus, Neptune, Pluto
    planet_velocities = [47.89, 35.03, 29.79, 24.13, 17.882, 13.06, 9.64, 6.81, 5.43, 4.74]
    
    min_vel = min(planet_velocities)
    max_vel = max(planet_velocities)
    
    # Map velocities to MIDI pitches (C1=24 to C6=84)
    planet_pitches = [int(map_scale(v, min_vel, max_vel, 24, 84)) for v in planet_velocities]
    
    # Tempo setup
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat

    # 2. Track Definitions
    tracks_config = [
        {
            "name": "Planet Piano (Melody 1)",
            "repeat": 8,
            "elong": 1.0, # Eighth Notes (0.5 beats base)
            "start": 0.0,
            "color": (0.8, 0.8, 1.0),
            "synth_params": [0.001, 0.6, 0.0] # Attack, Decay, Sustain
        },
        {
            "name": "Planet Flute (Melody 2)",
            "repeat": 3,
            "elong": 2.0, # Quarter Notes (1.0 beat)
            "start": 10.0,
            "color": (0.8, 1.0, 0.8),
            "synth_params": [0.1, 1.0, 0.5] # Slower attack for flute
        },
        {
            "name": "Planet Trumpet (Melody 3)",
            "repeat": 1,
            "elong": 4.0, # Half Notes (2.0 beats)
            "start": 20.0,
            "color": (1.0, 0.8, 0.8),
            "synth_params": [0.005, 1.0, 0.8] # Sharp attack for brass
        }
    ]

    base_dur = 0.5 # Base duration (EN)

    for config in tracks_config:
        track = project.add_track(name=config["name"])
        synth = track.add_fx("ReaSynth")
        if synth:
            synth.params[1] = config["synth_params"][0]
            synth.params[2] = config["synth_params"][1]
            synth.params[3] = config["synth_params"][2]

        item_end_beat = config["start"] + (len(planet_pitches) * base_dur * config["elong"] * config["repeat"])
        item = track.add_midi_item(config["start"] * spb, end=item_end_beat * spb)
        item.name = f"Planetary Canon - {config['name']}"
        take = item.active_take
        
        current_beat_offset = 0.0
        for r in range(config["repeat"]):
            for pitch in planet_pitches:
                dur = base_dur * config["elong"]
                # In MIDI items, start and end are relative to the item start if using Reapy's simplified API
                # But here we use absolute project seconds for take.add_note
                start_time = (config["start"] + current_beat_offset) * spb
                end_time = (config["start"] + current_beat_offset + dur * 0.95) * spb
                
                take.add_note(
                    pitch=pitch,
                    start=start_time,
                    end=end_time,
                    velocity=100,
                    channel=0
                )
                current_beat_offset += dur

    print("Celestial Canon (Harmonices Mundi) generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_celestial_canon()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
