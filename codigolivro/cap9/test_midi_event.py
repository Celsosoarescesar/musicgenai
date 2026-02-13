import reapy

# Thin wrapper test
try:
    res = reapy.RPR.MIDI_GetRecentInputEvent(0, 0, 0, 0, 0, 0)
    print(f"Result type: {type(res)}")
    print(f"Result value: {res}")
except Exception as e:
    print(f"Error: {e}")
