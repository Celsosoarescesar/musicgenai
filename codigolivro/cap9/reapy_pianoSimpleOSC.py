"""
reapy_pianoSimpleOSC.py

Demonstrates how to build a simple piano instrument playable
through sending OSC messages (e.g. from TouchOSC app).

Ported from pianoSimpleOSC.py
"""

import reapy
import time
import sys
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# Constants for MIDI messages
NOTE_ON = 0x90
NOTE_OFF = 0x80

# MIDI Note mapping
# Corresponds to C4, C#4, D4, etc.
NOTE_MAP = {
    "/1/push1": 60, # C4
    "/1/push2": 61, # C#4
    "/1/push3": 62, # D4
    "/1/push4": 63, # D#4
    "/1/push5": 64, # E4
    "/1/push6": 65, # F4
    "/1/push7": 66, # F#4
    "/1/push8": 67, # G4
    "/1/push9": 68, # G#4
    "/1/push10": 69, # A4
    "/1/push11": 70, # A#4
    "/1/push12": 71, # B4
    "/1/push13": 72  # C5
}

def play_note(address, *args):
    """
    Callback function called when a message about an OSC piano key arrives.
    If the OSC piano key is being pressed (value 1.0), it starts the corresponding note.
    If the OSC piano key is released (value 0.0), it stops the corresponding note.
    """
    if not args:
        return

    value = args[0]
    note = NOTE_MAP.get(address)
    
    if note is None:
        return

    if value == 1.0:
        # Note On
        status = NOTE_ON  # Channel 1 (0)
        reapy.RPR.StuffMIDIMessage(0, status, note, 100)
        print(f"Note On: {note} (Address: {address})")
    else:
        # Note Off
        status = NOTE_OFF # Channel 1 (0)
        reapy.RPR.StuffMIDIMessage(0, status, note, 0)
        print(f"Note Off: {note} (Address: {address})")

def main():
    try:
        # Check connection
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    ip = "0.0.0.0"
    port = 8000

    dispatcher = Dispatcher()
    # Register handlers for all keys in our map
    for address in NOTE_MAP.keys():
        dispatcher.map(address, play_note)

    server = BlockingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving at {ip}:{port}")
    print("Use an OSC client (e.g., TouchOSC) to send messages.")
    print("Addresses: /1/push1 (C4) to /1/push13 (C5)")
    print("Values: 1.0 (Note On), 0.0 (Note Off)")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OSC Server...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
