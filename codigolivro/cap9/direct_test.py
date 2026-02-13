import reapy

@reapy.inside_reaper()
def monitor():
    import reaper_python as RPR
    try:
        # In Python ReaScript, you MUST pass placeholders for all [out] parameters.
        # MIDI_GetRecentInputEvent has 6 parameters: index, status, d1, d2, time, devidx.
        # But wait, let's try calling it with just the index first.
        return RPR.RPR_MIDI_GetRecentInputEvent(0)
    except Exception as e:
        return f"Caught error: {e}"

print(monitor())
