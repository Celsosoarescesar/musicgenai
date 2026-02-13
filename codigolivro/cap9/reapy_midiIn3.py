import reapy
import time
import sys

def printEvent(event, channel, data1, data2):
    """
    Callback function that prints information about MIDI events.
    ported from midiIn3.py
    """
    if event == 176: # 0xB0: Control Change
        print(f"Got a Control Change (CC) message on channel {channel} with data values {data1} {data2}")
    elif event == 144: # 0x90: Note On
        print(f"Got a Note On message on channel {channel} for pitch {data1} and volume {data2}")
    elif (event == 128) or (event == 144 and data2 == 0): # 0x80: Note Off or Note On with vel 0
        print(f"Got a Note Off message on channel {channel} for pitch {data1}")
    else:
        print(f"Got another MIDI message: {event} {channel} {data1} {data2}")

def main():
    """
    Main function to monitor MIDI input using REAPER API (via reapy).
    """
    try:
        # Check connection
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    print("Monitoring MIDI Input on Device 0...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            # Poll for MIDI messages from hardware input 0
            # GetMIDIInputMessage returns (retval, buffer, timestamp)
            # We use a buffer size of 1024 (though messages are usually short)
            # The '0' is the device index. Change if needed.
            res = reapy.RPR.GetMIDIInputMessage(0, 1024, 0)
            
            if res[0]: # retval is True if message received
                msg = res[1]
                
                # REAPER returns a string of bytes or byte-like object
                # We need to handle potential string/byte differences in Python versions/REAPER
                if isinstance(msg, str):
                   # In some reapy versions/contexts it might be a string
                   status_byte = ord(msg[0])
                   data1 = ord(msg[1]) if len(msg) > 1 else 0
                   data2 = ord(msg[2]) if len(msg) > 2 else 0
                else: 
                   # bytes or bytearray
                   status_byte = msg[0]
                   data1 = msg[1] if len(msg) > 1 else 0
                   data2 = msg[2] if len(msg) > 2 else 0

                # Extract channel (lower nibble) and event type (upper nibble)
                # Channel is 0-15 in data, but usually 1-16 in display
                channel = (status_byte & 0x0F) + 1
                event_type = status_byte & 0xF0

                # Filter out active sensing (0xFE) or clock (0xF8) if necessary, 
                # but original script used ALL_EVENTS.
                # Only System Realtime messages (0xF8-0xFF) don't have channels.
                # For this script we focus on channel messages.
                if status_byte < 0xF0:
                    printEvent(event_type, channel, data1, data2)
                else:
                    # System messages
                    print(f"Got System Message: {status_byte}")

            # Short sleep to prevent high CPU usage
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nStopping MIDI monitor...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
