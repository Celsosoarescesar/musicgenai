import reapy

def create_full_project():
    # Conecta ao REAPER
    project = reapy.Project()
    
    # Limpa o projeto (Opcional - limpa todas as tracks para começar do zero)
    # for track in project.tracks:
    #     track.delete()
    
    # BPM e Configuração
    bpm = 120
    project.bpm = bpm
    
    # --- TRACK 1: DRUMS (Kick) ---
    drums_track = project.add_track(index=0, name="Drums")
    if not any("synth" in fx.name.lower() for fx in drums_track.fxs):
        fx = drums_track.add_fx("ReaSynth")
        # Ajusta ReaSynth para soar um pouco como um kick "low"
        # Nota: Configurar parâmetros via API é complexo, então usaremos o padrão
    
    drums_item = drums_track.add_midi_item(0, 4) # 4 segundos (1 compasso em 120BPM)
    drums_take = drums_item.active_take
    # Kick em cada tempo (beat)
    for i in range(4):
        drums_take.add_note(i, i + 0.5, 36, velocity=110) # 36 é C1 (Kick)

    # --- TRACK 2: BASS ---
    bass_track = project.add_track(index=1, name="Bass")
    if not any("synth" in fx.name.lower() for fx in bass_track.fxs):
        bass_track.add_fx("ReaSynth")
    
    bass_item = bass_track.add_midi_item(0, 4)
    bass_take = bass_item.active_take
    # Linha de baixo simples (notas C1, G1, A1, F1)
    bass_notes = [24, 31, 33, 29] # C1, G1, A1, F1
    for i, note in enumerate(bass_notes):
        bass_take.add_note(i, i + 1, note, velocity=90)

    # --- TRACK 3: MELODY ---
    mel_track = project.add_track(index=2, name="Melody")
    if not any("synth" in fx.name.lower() for fx in mel_track.fxs):
        mel_track.add_fx("ReaSynth")
    if not any("verb" in fx.name.lower() for fx in mel_track.fxs):
        mel_track.add_fx("ReaVerbate") # Adiciona um pouco de reverb
    
    mel_item = mel_track.add_midi_item(0, 4)
    mel_take = mel_item.active_take
    # Melodia simples em Dó Maior
    mel_notes = [60, 62, 64, 67, 65, 64, 62, 60]
    for i, note in enumerate(mel_notes):
        mel_take.add_note(i * 0.5, (i + 1) * 0.5, note, velocity=85)

    print("Projeto completo criado com sucesso!")
    print("3 Tracks: Drums, Bass, Melody.")
    print("Instrumentos (ReaSynth) e itens MIDI adicionados.")

if __name__ == "__main__":
    try:
        create_full_project()
    except Exception as e:
        print(f"Erro ao criar projeto: {e}")
