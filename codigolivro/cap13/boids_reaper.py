#
# This program simulates 2D boid behavior in REAPER using reapy.
# Boid positions and movements are mapped to musical notes.
#
# See http://www.red3d.com/cwr/boids/ and
# http://www.vergenet.net/~conrad/boids/pseudocode.html
#

import reapy
from math import sqrt
from random import randint, uniform

# Universe parameters
universeWidth = 1000   # temporal range (in beats)
universeHeight = 127   # MIDI pitch range (0-127)

# Boid generation parameters
numBoids = 50          # number of boids (musical voices)
numFrames = 100        # number of animation frames to simulate

# Boid distance parameters
minSeparation = 10     # min comfortable distance between two boids
flockThreshold = 30    # boids closer than this are in a local flock

# Boid behavior parameters (higher means quicker/stronger)
separationFactor = 0.01   # how quickly to separate
alignmentFactor = 0.16    # how quickly to align with local flockmates
cohesionFactor = 0.01     # how quickly to converge to attraction point
frictionFactor = 1.1      # how hard it is to move - the more, the harder
                          # (1.0 means no friction)

# Musical parameters
noteLength = 0.25      # length of each note in beats
timeScale = 0.1        # scale factor for time (X coordinate to beats)
pitchOffset = 36       # offset to bring pitches into musical range (C2)


### Define Boid class ###
class Boid:
    """
    A boid is a simplified bird (or other species) that lives in a flock.
    In this musical version, boid positions map to MIDI notes.
    """

    def __init__(self, x, y, initVelocityX=1, initVelocityY=1):
        """Initialize boid's position and initial velocity (x, y)."""
        
        # Set boid position
        self.coordinates = complex(x, y)  # boid coordinates (x, y)
        
        # Initialize boid velocity (x, y)
        self.velocity = complex(initVelocityX, initVelocityY)

    def sense(self, boids, center):
        """
        Sense other boids' positions, etc., and adjust velocity
        (i.e., the displacement of where to move next).
        """
        
        # Use individual rules of thumb to decide where to move next
        
        # 1. Rule of Separation - move away from other flockmates
        #                         to avoid crowding them
        self.separation = self.rule1_Separation(boids)
        
        # 2. Rule of Alignment - move towards the average heading
        #                        of other flockmates
        self.alignment = self.rule2_Alignment(boids)
        
        # 3. Rule of Cohesion - move toward the center of the universe
        self.cohesion = self.rule3_Cohesion(boids, center)
        
        # Create composite behavior
        self.velocity = (self.velocity / frictionFactor) + \
                        self.separation + self.alignment + \
                        self.cohesion

    def act(self):
        """Move boid to a new position using current velocity."""
        
        # Update coordinates
        self.coordinates = self.coordinates + self.velocity
        
        # Keep boids within bounds (wrap around)
        x = self.coordinates.real % universeWidth
        y = max(0, min(universeHeight, self.coordinates.imag))
        
        self.coordinates = complex(x, y)

    ##### Steering behaviors ####################
    def rule1_Separation(self, boids):
        """Return proper velocity to keep separate from other boids,
           i.e., avoid collisions.
        """
        
        newVelocity = complex(0, 0)  # holds new velocity
        
        # Get distance from every other boid in the flock, and as long
        # as we are too close for comfort, calculate direction to
        # move away
        for boid in boids:  # for each boid
            
            separation = self.distance(boid)  # how far are we?
            
            # Too close for comfort (excluding ourself)?
            if separation < minSeparation and boid != self:
                # Yes, so let's move away from this boid
                newVelocity = newVelocity - \
                              (boid.coordinates - self.coordinates)
        
        return newVelocity * separationFactor  # return new velocity

    def rule2_Alignment(self, boids):
        """Return proper velocity to move in the same general direction
           as local flockmates.
        """
        
        totalVelocity = complex(0, 0)  # holds sum of boid velocities
        numLocalFlockmates = 0         # holds count of local flockmates
        
        # Iterate through all the boids looking for local flockmates,
        # and accumulate all their velocities
        for boid in boids:
            
            separation = self.distance(boid)  # get boid distance
            
            # If this is a local flockmate, record its velocity
            if separation < flockThreshold and boid != self:
                totalVelocity = totalVelocity + boid.velocity
                numLocalFlockmates = numLocalFlockmates + 1
        
        # Average flock velocity (excluding ourselves)
        if numLocalFlockmates > 0:
            avgVelocity = totalVelocity / numLocalFlockmates
        else:
            avgVelocity = totalVelocity
        
        # Adjust velocity by how quickly we want to align
        newVelocity = avgVelocity - self.velocity
        
        return newVelocity * alignmentFactor  # return new velocity

    def rule3_Cohesion(self, boids, center):
        """Return proper velocity to bring us closer to center of the
           universe.
        """
        
        newVelocity = center - self.coordinates
        
        return newVelocity * cohesionFactor  # return new velocity

    ##### Helper function ####################
    def distance(self, other):
        """Calculate the Euclidean distance between this and
           another boid.
        """
        
        xDistance = (self.coordinates.real - other.coordinates.real)
        yDistance = (self.coordinates.imag - other.coordinates.imag)
        
        return sqrt(xDistance * xDistance + yDistance * yDistance)


### Main REAPER integration ###
def create_boid_music():
    """Create musical composition based on boid flocking behavior."""
    
    # Connect to REAPER
    project = reapy.Project()
    
    # Create a new MIDI track
    track = project.add_track(name="Boid Flocking")
    
    # Create a MIDI item on the track
    # reapy uses start and end parameters (in seconds)
    item_length = numFrames * timeScale
    item = track.add_midi_item(start=0, end=item_length)
    
    # Get the take (MIDI data container)
    take = item.active_take
    
    # Initialize boid universe
    boids = []
    attractPoint = complex(universeWidth / 2, universeHeight / 2)
    
    # Create and place boids with random positions and velocities
    for i in range(numBoids):
        # Get random position for this boid
        x = randint(0, universeWidth)
        y = randint(0, universeHeight)
        
        # Random initial velocity
        vx = uniform(-2, 2)
        vy = uniform(-2, 2)
        
        # Create a boid with random position and velocity
        boid = Boid(x, y, vx, vy)
        boids.append(boid)
    
    # Simulate boid movement and create notes
    notes_data = []  # Collect all notes first
    
    for frame in range(numFrames):
        
        # Sensing and acting loop for all boids
        for boid in boids:
            
            # First observe other boids and decide how to adjust movement
            boid.sense(boids, attractPoint)
            
            # Then move!
            boid.act()
            
            # Create a MIDI note based on boid position
            # X coordinate -> time (in beats)
            # Y coordinate -> pitch
            time = frame * timeScale
            pitch = int(boid.coordinates.imag) + pitchOffset
            
            # Ensure pitch is in valid MIDI range (0-127)
            pitch = max(0, min(127, pitch))
            
            # Velocity based on boid's movement speed
            speed = abs(boid.velocity)
            velocity = int(min(127, max(40, speed * 20)))
            
            # Store note data
            notes_data.append({
                'pitch': pitch,
                'start': time,
                'end': time + noteLength,
                'velocity': velocity
            })
    
    # Add all notes to the MIDI take
    for note in notes_data:
        take.add_note(
            pitch=note['pitch'],
            start=note['start'],
            end=note['end'],
            velocity=note['velocity']
        )
    
    print(f"Created {numBoids} boid voices over {numFrames} frames")
    print(f"Total notes: {len(notes_data)}")
    print(f"Total duration: {numFrames * timeScale} beats")
    print("Boid flocking music generated successfully!")


# Run the script
if __name__ == "__main__":
    try:
        print("Connecting to REAPER...")
        create_boid_music()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure REAPER is running and reapy is properly configured.")
        print("You may need to run 'reapy.config.enable_dist_api()' from inside REAPER first.")

