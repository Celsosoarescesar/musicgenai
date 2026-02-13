import reapy
import random
import os
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: The 'Pillow' library is required. Please install it with: pip install Pillow")
    Image = None

def map_value(val, in_min, in_max, out_min, out_max):
    if in_max == in_min: return out_min
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def quantize_to_mixolydian(pitch):
    # C Mixolydian: C, D, E, F, G, A, Bb (0, 2, 4, 5, 7, 9, 10)
    scale = [0, 2, 4, 5, 7, 9, 10]
    octave = pitch // 12
    note = pitch % 12
    closest = min(scale, key=lambda x: abs(x - note))
    return (octave * 12) + closest

def create_dummy_image(path):
    if Image is None: return
    print(f"Generating test image: {path}")
    img = Image.new('RGB', (300, 300))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # Red gradient horizontally, Blue vertically
            pixels[i, j] = (i % 256, (i+j) % 256, j % 256)
    img.save(path)

def create_image_sonification():
    if Image is None: return

    # Connect to REAPER
    project = reapy.Project()
    project.bpm = 60.0
    spb = 1.0 # 60 BPM = 1 sec per beat

    # Image logic
    image_path = os.path.join(os.path.dirname(__file__), "soundscapeLoutrakiSunset.jpg")
    if not os.path.exists(image_path):
        create_dummy_image(image_path)

    img = Image.open(image_path)
    width, height = img.size
    
    # Selected rows to sonify (as suggested in original script)
    pixel_rows = [0, height // 4, height // 2, (3 * height) // 4, height - 1]
    
    # Musical Parameters
    min_duration, max_duration = 0.8, 6.0
    time_displacements = [0.75, 0.5, 0.25, 0.125] # DEN, EN, SN, TN

    # REAPER Setup
    track = project.add_track(name="Loutraki Image Soundscape")
    synth = track.add_fx("ReaSynth")
    if synth:
        synth.params[1] = 0.05 # Soft attack
        synth.params[2] = 0.8  # Long decay

    # Create a MIDI item long enough for all columns
    # Every column is 1 beat + displacement
    total_beats = width + max_duration + 1 
    item = track.add_midi_item(0, end=total_beats * spb)
    item.name = f"Sonification of {os.path.basename(image_path)}"
    take = item.active_take

    print(f"Sonifying {len(pixel_rows)} rows of {width} pixels each...")

    for row_y in pixel_rows:
        for col_x in range(width):
            r, g, b = img.getpixel((col_x, row_y))
            
            # 1. Luminosity -> Pitch
            lum = (r + g + b) / 3
            raw_pitch = map_value(lum, 0, 255, 36, 96) # C2 to C7
            pitch = quantize_to_mixolydian(int(raw_pitch))
            
            # 2. Red -> Duration
            dur = map_value(r, 0, 255, min_duration, max_duration)
            
            # 3. Blue -> Velocity
            vel = map_value(b, 0, 255, 40, 110)
            
            # Start Time = column + random displacement
            start_beat = float(col_x) + random.choice(time_displacements)
            
            take.add_note(
                pitch=int(pitch),
                start=float(start_beat * spb),
                end=float((start_beat + dur) * spb),
                velocity=int(vel),
                channel=0
            )

    print("Image sonification generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_image_sonification()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
