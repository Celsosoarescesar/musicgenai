#
# musicalSphere_reaper.py
#
# Demonstrates how to create a musical composition based on a 3D rotating sphere.
# The sphere is modeled using points on a spherical coordinate system.
# When a point passes the primary meridian (the imaginary vertical line closest
# to the viewer), a note is played based on its latitude (low to high pitch).
#
# This version creates MIDI notes in REAPER instead of playing them in real-time.
#
# Based on code by Uri Wilensky (1998), distributed with NetLogo
# under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.
#

import reapy
from random import random, randint
from math import sin, cos, pi

# Musical parameters
SCALE = [0, 2, 4, 5, 7, 9, 11]  # Major scale intervals
LOW_PITCH = 36   # C2
HIGH_PITCH = 96  # C7
NOTE_DURATION = 0.5  # in beats

# Sphere parameters
RADIUS = 200
NUM_POINTS = 200
VELOCITY = 0.01  # angular velocity per frame
NUM_FRAMES = 1000  # how many frames to simulate
TIME_SCALE = 0.05  # frame to beats conversion


def map_value(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_to_scale(value, in_min, in_max, low_pitch, high_pitch, scale):
    """Map a value to a pitch within a musical scale."""
    # First map to the pitch range
    pitch = map_value(value, in_min, in_max, low_pitch, high_pitch)
    
    # Round to nearest scale degree
    octave = int(pitch / 12)
    pitch_class = int(pitch % 12)
    
    # Find closest note in scale
    closest = min(scale, key=lambda x: abs(x - pitch_class))
    
    return octave * 12 + closest


def spherical_to_cartesian(r, phi, theta):
    """Convert spherical to cartesian coordinates."""
    # Adjust rotation so that theta is 0 at max z (i.e., closest to viewer)
    x = r * sin(phi) * cos(theta + pi/2)
    y = r * cos(phi)
    z = r * sin(phi) * sin(theta + pi/2)
    
    return x, y, z


class MusicalSphere:
    """Creates a revolving sphere that generates musical notes."""
    
    def __init__(self, radius, num_points, velocity, num_frames):
        """
        Construct a revolving sphere with given 'radius', 'num_points'
        number of points (all on the surface), moving with 'velocity' angular
        (theta / azimuthal) velocity, for 'num_frames' frames.
        """
        
        self.radius = radius
        self.num_points = num_points
        self.velocity = velocity
        self.num_frames = num_frames
        
        # Sphere data structure (parallel lists)
        self.theta_values = []  # holds the points' rotation (azimuthal angle)
        self.phi_values = []    # holds the points' latitude (polar angle)
        
        # Notes data
        self.notes = []  # will store all notes to be created
        
        self.init_sphere()
    
    def init_sphere(self):
        """Generate a sphere of 'radius' out of points (placed on the surface)."""
        
        for i in range(self.num_points):
            # Get random spherical coordinates for this point
            r = self.radius  # all points are placed *on* the surface
            theta = map_value(random(), 0.0, 1.0, 0.0, 2*pi)  # random rotation
            phi = map_value(random(), 0.0, 1.0, 0.0, pi)      # random latitude
            
            # Remember this point's spherical coordinates
            self.phi_values.append(phi)
            self.theta_values.append(theta)
    
    def simulate(self):
        """Rotate points and generate notes when crossing the primary meridian."""
        
        for frame in range(self.num_frames):
            # Current time in beats
            time = frame * TIME_SCALE
            
            for i in range(self.num_points):
                # Get current theta and phi
                old_theta = self.theta_values[i]
                phi = self.phi_values[i]
                
                # Increment angle to simulate rotation
                new_theta = (old_theta + self.velocity) % (2*pi)
                
                # Did we just cross the primary meridian?
                if old_theta > new_theta:
                    # Yes! Generate a note based on latitude (phi)
                    pitch = map_to_scale(phi, 0, pi, LOW_PITCH, HIGH_PITCH, SCALE)
                    velocity = randint(60, 100)  # random velocity
                    
                    # Store note data
                    self.notes.append({
                        'pitch': pitch,
                        'start': time,
                        'end': time + NOTE_DURATION,
                        'velocity': velocity
                    })
                
                # Update theta
                self.theta_values[i] = new_theta
        
        return self.notes


def create_musical_sphere():
    """Create musical composition based on rotating sphere in REAPER."""
    
    print("Initializing musical sphere...")
    
    # Create the sphere and simulate
    sphere = MusicalSphere(
        radius=RADIUS,
        num_points=NUM_POINTS,
        velocity=VELOCITY,
        num_frames=NUM_FRAMES
    )
    
    print(f"Simulating {NUM_FRAMES} frames with {NUM_POINTS} points...")
    notes = sphere.simulate()
    
    print(f"Generated {len(notes)} notes")
    
    # Connect to REAPER
    print("Connecting to REAPER...")
    project = reapy.Project()
    
    # Create a new MIDI track
    track = project.add_track(name="Musical Sphere")
    
    # Calculate total duration
    total_duration = NUM_FRAMES * TIME_SCALE + NOTE_DURATION
    
    # Create a MIDI item on the track
    item = track.add_midi_item(start=0, end=total_duration)
    
    # Get the take (MIDI data container)
    take = item.active_take
    
    # Add all notes to the MIDI take
    print("Creating MIDI notes in REAPER...")
    for note in notes:
        take.add_note(
            pitch=note['pitch'],
            start=note['start'],
            end=note['end'],
            velocity=note['velocity']
        )
    
    print(f"\n✓ Musical Sphere created successfully!")
    print(f"  - Track: Musical Sphere")
    print(f"  - Total notes: {len(notes)}")
    print(f"  - Duration: {total_duration:.2f} beats")
    print(f"  - Sphere radius: {RADIUS}")
    print(f"  - Points: {NUM_POINTS}")
    print(f"  - Frames simulated: {NUM_FRAMES}")


# Run the script
if __name__ == "__main__":
    try:
        print("=" * 60)
        print("MUSICAL SPHERE - REAPER Generator")
        print("=" * 60)
        create_musical_sphere()
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure REAPER is running and reapy is properly configured.")
        print("You may need to run 'reapy.config.enable_dist_api()' from inside REAPER first.")
