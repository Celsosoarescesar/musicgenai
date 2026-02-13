import reapy

def create_magenta_track(project, melody, track_name="Magenta Generated"):
    """
    Cria uma track no REAPER e insere a melodia gerada.
    """
    print(f"Conectando ao REAPER e criando track: {track_name}")
    
    # Adiciona a track
    track = project.add_track(name=track_name)
    
    # Adiciona FX ReaSynth para podermos ouvir algo
    if not any("synth" in fx.name.lower() for fx in track.fxs):
        track.add_fx("ReaSynth")
        
    # Calcula o tempo total para o item MIDI
    total_duration = max(note['end'] for note in melody) if melody else 4
    
    # Adiciona o item MIDI
    midi_item = track.add_midi_item(0, total_duration)
    take = midi_item.active_take
    
    # Adiciona as notas
    for note in melody:
        take.add_note(
            start=note['start'],
            end=note['end'],
            pitch=note['pitch'],
            velocity=note['velocity']
        )
        
    print(f"Track '{track_name}' criada com {len(melody)} notas.")
    return track

if __name__ == "__main__":
    # Teste simples isolado
    try:
        project = reapy.Project()
        dummy_melody = [{'start': 0, 'end': 1, 'pitch': 60, 'velocity': 100}]
        create_magenta_track(project, dummy_melody, "Integration Test")
    except Exception as e:
        print(f"Erro no teste de integração: {e}")
