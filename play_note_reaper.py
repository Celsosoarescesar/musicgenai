import reapy

def play_note_reaper():
    # Conecta ao REAPER
    # Certifique-se de que o REAPER está aberto e o reapy configurado
    project = reapy.Project()
    
    # Adiciona uma nova trilha ou usa a primeira existente
    if len(project.tracks) == 0:
        track = project.add_track()
    else:
        track = project.tracks[0]
        
    track.name = "Python Note"
    
    # Cria um MIDI item que dura 2 segundos (HN - Half Note aproximado)
    # Posição inicial: 0.0, Fim: 2.0
    item = track.add_midi_item(0, 2)
    
    # Pega o take do item (onde as notas MIDI ficam)
    take = item.active_take
    
    # Adiciona a nota C4 (Dó Central)
    # MIDI note number para C4 é 60
    # Start: 0.0, End: 1.0 (em segundos, dependendo da configuração do projeto)
    # Velocity: 100
    take.add_note(0, 1, 60, velocity=100)
    
    print("Nota C4 adicionada ao projeto no REAPER!")

if __name__ == "__main__":
    try:
        play_note_reaper()
    except Exception as e:
        print(f"Erro: {e}")
        print("Verifique se o REAPER está aberto e se o reapy está configurado corretamente.")
