"""
reapy_midiSynthesizer.py

A simple MIDI synthesizer which plays notes originating on an external MIDI controller.
Instead of an internal synth, we forward the notes to REAPER's active instrument 
(Virtual MIDI Keyboard) using StuffMIDIMessage.

Ported from midiSynthesizer.py
"""

import reapy
import time
import sys
import mido

# Constants for MIDI messages
NOTE_ON = 0x90
NOTE_OFF = 0x80

def beginNote(channel, note, velocity):
    """
    Start this note on internal MIDI synthesizer.
    In REAPER/reapy, we send a Note On message to the Virtual MIDI Keyboard.
    """
    # 0 = Virtual MIDI Keyboard
    # msg1 = Status byte (Note On + Channel 0-15)
    # msg2 = Note Number
    # msg3 = Velocity
    
    # Ensure channel is 0-15
    status = NOTE_ON | (channel & 0x0F)
    
    # StuffMIDIMessage(mode, msg1, msg2, msg3)
    # mode 0: Virtual MIDI Keyboard
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)
    # print(f"Note On: {note} vel: {velocity} ch: {channel}")

def endNote(channel, note, velocity):
    """
    Stop this note on internal MIDI synthesizer.
    In REAPER/reapy, we send a Note Off message.
    """
    # Ensure channel is 0-15
    status = NOTE_OFF | (channel & 0x0F)
    
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)
    # print(f"Note Off: {note} vel: {velocity} ch: {channel}")


def main():
    try:
        # Check connection
        project = reapy.Project()
        print("Connected to REAPER. Redirecting MIDI to Virtual Keyboard...")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    print("Available MIDI Input Ports:")
    input_ports = mido.get_input_names()
    for i, name in enumerate(input_ports):
        print(f"{i}: {name}")

    if not input_ports:
        print("No MIDI input ports found.")
        return

    # Use the first available port or ask user to specify
    port_name = input_ports[0] 
    print(f"\nOpening MIDI Input: {port_name}")
    print("Ensure a track is armed and monitoring the Virtual MIDI Keyboard or All Inputs.")
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
        print("\nStopping MIDI synthesizer...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
