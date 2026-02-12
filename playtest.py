import reapy

def play_note_with_sound():
    project = reapy.Project()
    
    if len(project.tracks) == 0:
        track = project.add_track()
    else:
        track = project.tracks[0]
        
    track.name = "Python Note"
    
    # ADICIONA O SINTETIZADOR BÁSICO DO REAPER
    # Se já não houver um instrumento, adiciona o ReaSynth
    if not any("synth" in fx.name.lower() for fx in track.fxs):
        track.add_fx("ReaSynth")
    
    # Cria o item MIDI e a nota
    item = track.add_midi_item(0, 2)
    take = item.active_take
    take.add_note(0, 1, 60, velocity=100)
    
    print("Nota adicionada com ReaSynth! Certifique-se de que o [audio device closed] sumiu no topo do REAPER.")

if __name__ == "__main__":
    try:
        play_note_with_sound()
    except Exception as e:
        print(f"Erro: {e}")