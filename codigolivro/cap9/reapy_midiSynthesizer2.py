"""
reapy_midiSynthesizer2.py

A simple MIDI synthesizer which plays notes originating on an external MIDI controller.
This version includes a way to change MIDI sounds (instruments), by turning one of the
controller knobs (CC 16).

Ported from midiSynthesizer2.py
"""

import reapy
import time
import sys
import mido

# Constants for MIDI messages
NOTE_ON = 0x90
NOTE_OFF = 0x80
PROGRAM_CHANGE = 0xC0

# Knob for changing instruments
# (same as data1 value sent when turning this knob on the MIDI controller)
KNOB_CC = 16

def beginNote(channel, note, velocity):
    """
    Start this note on internal MIDI synthesizer.
    """
    status = NOTE_ON | (channel & 0x0F)
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)

def endNote(channel, note, velocity):
    """
    Stop this note on internal MIDI synthesizer.
    """
    status = NOTE_OFF | (channel & 0x0F)
    reapy.RPR.StuffMIDIMessage(0, status, note, velocity)

def changeInstrument(channel, instrument):
    """
    Change the instrument (Program Change).
    """
    # Program Change message: Status (0xC0 | channel), Data1 (Program #), Data2 (0)
    status = PROGRAM_CHANGE | (channel & 0x0F)
    
    # StuffMIDIMessage(mode, msg1, msg2, msg3)
    reapy.RPR.StuffMIDIMessage(0, status, instrument, 0)
    
    print(f"Instrument set to Program #{instrument}")

def main():
    try:
        # Check connection
        project = reapy.Project()
        print("Connected to REAPER.")
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

    # Use the first available port
    port_name = input_ports[0] 
    print(f"\nOpening MIDI Input: {port_name}")
    print(f"Turn CC Controller #{KNOB_CC} to change instruments.")
    print("Ensure a track with a GM-compatible synth is armed.")
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
                elif msg.type == 'control_change':
                    if msg.control == KNOB_CC:
                        changeInstrument(msg.channel, msg.value)

    except KeyboardInterrupt:
        print("\nStopping MIDI synthesizer...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
