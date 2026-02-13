import reapy
import time

def print_note(pitch, volume):
    """Callback function called when a Note On event is detected."""
    print(f"pitch = {pitch} volume = {volume}")

def main():
    """
    Ported version of midiIn1.py using reapy.
    Listens for MIDI input from the hardware device (index 0) and prints
    pitch and volume for Note On messages.
    """
    try:
        # Check if reapy is connected
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER. Make sure REAPER is open and reapy is configured.")
        return

    print("Checking for MIDI Input from Device 0 (External Keyboard)...")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # Poll for MIDI messages from hardware input index 0
            # GetMIDIInputMessage returns (bool success, str msg, float frame_offset)
            # In reapy, the msg is usually returned as a character string or tuple of bytes.
            
            # Using RPR.GetMIDIInputMessage directly
            res = reapy.RPR.GetMIDIInputMessage(0, 1024, 0)
            
            if res[0]: # Success
                msg = res[1]
                # In reapy/Python 3, the message might need conversion 
                # to get the status byte and data bytes.
                
                # REAPER's buffer usually contains the MIDI message bytes.
                # If msg is a string of bytes:
                if isinstance(msg, (bytes, bytearray)):
                    status = msg[0]
                    data1 = msg[1]
                    data2 = msg[2]
                else:
                    # If it's returned as a string (legacy behavior or specific wrapper)
                    status = ord(msg[0])
                    data1 = ord(msg[1])
                    data2 = ord(msg[2])

                # Check if it's a Note On (0x90 to 0x9F for channels 1-16)
                # and volume (data2) > 0. Some keyboards send Note On with vol 0 for Note Off.
                if (status & 0xF0) == 0x90 and data2 > 0:
                    print_note(data1, data2)
                
            # Sleep briefly to avoid slamming the CPU
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\nStopping MIDI monitor...")
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
