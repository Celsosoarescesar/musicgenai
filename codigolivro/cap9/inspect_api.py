import reapy
import inspect

@reapy.inside_reaper()
def get_sig():
    import reascript_api as RPR
    try:
        # Some ReaScript functions might not support inspect, so we use dir or trial/error
        func = getattr(RPR, 'RPR_MIDI_GetRecentInputEvent', None)
        if func:
            return f"Found: {func}"
        return "Not found"
    except Exception as e:
        return str(e)

print(get_sig())
