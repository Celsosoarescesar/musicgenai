import random

def generate_melody(length=16, scale=[60, 62, 64, 65, 67, 69, 71, 72]):
    """
    Simula uma geração da Magenta. 
    Em um ambiente real com Magenta instalado, usaríamos:
    from magenta.models.melody_rnn import melody_rnn_sequence_generator
    """
    print(f"Gerando melodia de {length} notas...")
    
    melody = []
    current_time = 0.0
    
    for _ in range(length):
        note = random.choice(scale)
        duration = random.choice([0.25, 0.5, 1.0])
        velocity = random.randint(70, 110)
        
        melody.append({
            'start': current_time,
            'end': current_time + duration,
            'pitch': note,
            'velocity': velocity
        })
        
        current_time += duration
        
    return melody

if __name__ == "__main__":
    test_melody = generate_melody()
    for note in test_melody:
        print(f"Nota: {note['pitch']} | Start: {note['start']} | End: {note['end']}")
