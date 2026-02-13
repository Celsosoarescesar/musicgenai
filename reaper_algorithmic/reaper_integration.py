import reapy

def create_markov_track(project, sequence, track_name="Markov Stochastic"):
    """
    Insere notas geradas via Algoritmo de Markov no REAPER.
    """
    print(f"Criando track no REAPER: {track_name}")
    track = project.add_track(name=track_name)
    
    # Adiciona ReaSynth se não houver FX
    if not any("synth" in fx.name.lower() for fx in track.fxs):
        track.add_fx("ReaSynth")
        
    total_len = max(n['end'] for n in sequence) if sequence else 4
    item = track.add_midi_item(0, total_len)
    take = item.active_take
    
    for note in sequence:
        take.add_note(
            start=note['start'],
            end=note['end'],
            pitch=note['pitch'],
            velocity=note['velocity']
        )
    
    print(f"Sucesso: {len(sequence)} notas adicionadas à track '{track_name}'.")
    return track
