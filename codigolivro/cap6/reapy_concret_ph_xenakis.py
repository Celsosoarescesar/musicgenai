import reapy
import random

def create_concret_ph_xenakis():
    # Connect to REAPER
    project = reapy.Project()
    
    # Constants for controlling musical parameters
    cloud_width = 64.0        # duration in beats
    cloud_density = 23.44     # density of the cloud
    particle_duration = 0.2   # max duration of each sound particle
    num_particles = int(cloud_density * cloud_width) # ~1500 particles
    
    tempo = project.bpm
    if not tempo or tempo == 0:
        tempo = 120.0
    spb = 60.0 / tempo # Seconds per beat
    
    # REAPER Integration
    track = project.add_track(name="Xenakis Cloud (Concret PH)")
    synth = track.add_fx("ReaSynth")
    if synth:
        # Fast "clicky" sound
        synth.params[1] = 0.001 # Attack
        synth.params[2] = 0.1   # Decay
        
    print(f"Generating {num_particles} particles over {cloud_width} beats...")
    
    # We need to know the total duration to create the MIDI item
    # Max start time is cloud_width, max duration is particle_duration
    total_duration_beats = cloud_width + particle_duration
    
    # Create one large MIDI item for the cloud
    item = track.add_midi_item(0, end=total_duration_beats * spb)
    item.name = "Granular Cloud"
    take = item.active_take
    
    # Implementation of fade out at the last 20 beats
    fade_start = cloud_width - 20.0
    
    for i in range(num_particles):
        # Create random attributes
        pitch = random.randint(0, 127)
        start_beat = random.random() * cloud_width
        duration_beats = random.random() * particle_duration
        
        # Base velocity
        velocity = random.randint(30, 110)
        
        # Apply pseudo-fadeOut in the last 20 beats
        if start_beat > fade_start:
            # Linear factor from 1.0 (at fade_start) to 0.0 (at cloud_width)
            fade_factor = (cloud_width - start_beat) / 20.0
            velocity = int(velocity * fade_factor)
            
        # Ensure velocity is within MIDI bounds
        velocity = max(0, min(127, velocity))
        
        if velocity > 0:
            take.add_note(
                pitch=int(pitch),
                start=float(start_beat * spb),
                end=float((start_beat + duration_beats) * spb),
                velocity=int(velocity),
                channel=0
            )
            
    print("Xenakis granular cloud generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_concret_ph_xenakis()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
