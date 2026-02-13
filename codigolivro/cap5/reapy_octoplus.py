import reapy

def create_octoplus_effect():
    # Connect to REAPER
    project = reapy.Project()
    
    # Program constants
    tempo = 110.0
    project.bpm = tempo
    
    # Test melody - riff from Deep Purple's "Smoke on the Water"
    # G2, AS2, C3, G2, AS2, CS3, C3, G2, AS2, C3, AS2, G2
    # MIDI: 43, 46, 48, 43, 46, 49, 48, 43, 46, 48, 46, 43
    pitches = [43, 46, 48, 43, 46, 49, 48, 43, 46, 48, 46, 43]
    # Durations (beats): QN=1.0, DQN=1.5, EN=0.5, HN=2.0, DHN+EN=3.5
    durs = [1.0, 1.0, 1.5, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.5, 1.0, 3.5]
    
    spb = 60.0 / tempo # Seconds per beat

    def setup_track(name):
        track = project.add_track(name=name)
        synth = track.add_fx("ReaSynth")
        if synth:
            # Adjust ReaSynth for a more "guitar-like" pluck/bass sound
            # (Attack, Decay, Sustain, Release parameters vary by ReaSynth version, 
            # but usually 1=Attack, 2=Decay)
            synth.params[1] = 0.01 # Fast attack
            synth.params[2] = 0.4  # Short decay
        return track

    # 1. Original Phrase
    orig_track = setup_track("Smoke Original")
    total_beats = sum(durs)
    orig_item = orig_track.add_midi_item(0, end=total_beats * spb)
    orig_item.name = "Original Riff"
    orig_take = orig_item.active_take
    
    cursor = 0.0
    for p, d in zip(pitches, durs):
        orig_take.add_note(pitch=int(p), start=cursor * spb, end=(cursor + d * 0.9) * spb, velocity=100)
        cursor += d

    # 2. Octoplus Effect Phrase (Original + Octave lower + Fifth lower)
    effect_track = setup_track("Smoke Octoplus (Effect)")
    # Start after original + 2 beats gap
    start_offset = total_beats + 2.0
    effect_item = effect_track.add_midi_item(start_offset * spb, end=(start_offset + total_beats) * spb)
    effect_item.name = "Octoplus Riff"
    effect_take = effect_item.active_take
    
    cursor = 0.0
    for p, d in zip(pitches, durs):
        # chordPitches = [pitch, pitch - 12, pitch - 5]
        chord_pitches = [p, p - 12, p - 5]
        for cp in chord_pitches:
            effect_take.add_note(pitch=int(cp), start=cursor * spb, end=(cursor + d * 0.9) * spb, velocity=90)
        cursor += d

    print("Octoplus effect generated in REAPER successfully.")

if __name__ == "__main__":
    try:
        create_octoplus_effect()
    except Exception as e:
        print(f"Error: {e}")
        print("Ensure REAPER is open and reapy is configured.")
