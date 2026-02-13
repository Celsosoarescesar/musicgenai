import reapy

def create_torch_track(project, melody, track_name="Torch Neural Gen"):
    """
    Insere notas geradas via PyTorch no REAPER.
    """
    print(f"Criando track no REAPER: {track_name}")
    track = project.add_track(name=track_name)
    
    # Adiciona ReaSynth se não houver FX
    if not any("synth" in fx.name.lower() for fx in track.fxs):
        track.add_fx("ReaSynth")
        
    total_len = max(n['end'] for n in melody) if melody else 4
    item = track.add_midi_item(0, total_len)
    take = item.active_take
    
    for note in melody:
        take.add_note(
            start=note['start'],
            end=note['end'],
            pitch=note['pitch'],
            velocity=note['velocity']
        )
    
    print(f"Sucesso: {len(melody)} notas adicionadas à track '{track_name}'.")
    return track
