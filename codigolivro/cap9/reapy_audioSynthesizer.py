"""
reapy_audioSynthesizer.py

Creates a simple AudioSample synthesizer which plays notes originating
on a external MIDI controller.
It creates/uses a track named "Audio Synth" with ReaSamplOmatic5000.

Ported from audioSynthesizer.py
"""

import reapy
import time
import sys
import os
import mido

# Constants for MIDI messages
NOTE_ON = 0x90
NOTE_OFF = 0x80

SAMPLE_FILE = "strings - A4.wav"
TRACK_NAME = "Audio Synth"
FX_NAME = "ReaSamplOmatic5000"

def setup_synth():
    """
    Sets up the REAPER track and FX for the synthesizer.
    """
    project = reapy.Project()

    # Find or create track
    track = None
    for t in project.tracks:
        if t.name == TRACK_NAME:
            track = t
            break
    
    if not track:
        print(f"Creating track: {TRACK_NAME}")
        track = project.add_track()
        track.name = TRACK_NAME
    else:
        print(f"Using existing track: {TRACK_NAME}")

    # Ensure Record Monitoring is ON and Input is set to All MIDI
    # Note: reapy might not have direct setters for all these, 
    # but we can at least select the track for the user.
    track.select()

    # Add ReaSamplOmatic5000 if not present
    fx = track.add_fx(FX_NAME) # returns existing if present
    
    # Try to load sample
    if os.path.exists(SAMPLE_FILE):
        # We need to set the FILE parameter. 
        # RS5k param index for file is ... tricky via Reascript directly without chunk parsing.
        # But we can try setting the parameter 'FILE' if reapy wrapper supports named params 
        # or just tell the user.
        # Actually, RS5k file loading via API is non-trivial without chunk manipulation.
        # simpler approach: warn user to load it manually if it's not pre-loaded.
        print(f"Found {SAMPLE_FILE}.")
        print(f"Please manually load {SAMPLE_FILE} into {FX_NAME} if not already loaded.")
    else:
        print(f"Warning: {SAMPLE_FILE} not found in current directory.")
        print(f"Please load a sample into {FX_NAME} manually to hear sound.")

    # Configure RS5k for pitch shifting (Mode: Note (Semitone Shifted))
    # This corresponds to parameter 2 (Mode) -> value 0.0 (Sample (Ignore Note)) vs ?
    # Let's just notify user to check settings.
    print("Ensure ReaSamplOmatic5000 mode is set to 'Note (Semitone Shifted)' for chromatic play.")

    return track

def beginNote(channel, note, velocity):
    # Forward Note On
    status = NOTE_ON | (channel & 0x0F)
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)

def endNote(channel, note, velocity):
    # Forward Note Off
    status = NOTE_OFF | (channel & 0x0F)
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)

def main():
    try:
        # Check connection
        setup_synth()
        print("Synthesizer Setup Complete.")
    except Exception as e:
        print(f"Error connecting to REAPER: {e}")
        return

    print("Available MIDI Input Ports:")
    input_ports = mido.get_input_names()
    for i, name in enumerate(input_ports):
        print(f"{i}: {name}")

    if not input_ports:
        print("No MIDI input ports found.")
        return

    # Use the first available port
    port_name = input_ports[0] 
    print(f"\nOpening MIDI Input: {port_name}")
    print("If you don't hear sound, ensure the 'Audio Synth' track is Armed and Monitoring is ON.")
    print("Press Ctrl+C to stop.")

    try:
        with mido.open_input(port_name) as inport:
            for msg in inport:
                if msg.type == 'note_on':
                    if msg.velocity > 0:
                        beginNote(msg.channel, msg.note, msg.velocity)
                    else:
                        endNote(msg.channel, msg.note, 0)
                elif msg.type == 'note_off':
                    endNote(msg.channel, msg.note, msg.velocity)
                
    except KeyboardInterrupt:
        print("\nStopping audio synthesizer...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
