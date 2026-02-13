import random

class MarkovMusicGenerator:
    def __init__(self):
        # Probabilidades de transição simples (C -> D: 60%, C -> E: 20%, C -> G: 20%)
        # Notas representadas por números MIDI
        self.transitions = {
            60: [62, 62, 62, 64, 67], # C4 -> D4, E4, G4
            62: [64, 64, 65, 60],     # D4 -> E4, F4, C4
            64: [65, 67, 60],         # E4 -> F4, G4, C4
            65: [67, 62, 60],         # F4 -> G4, D4, C4
            67: [60, 69, 72],         # G4 -> C4, A4, C5
            69: [72, 67, 65],         # A4 -> C5, G4, F4
            72: [60, 67, 69]          # C5 -> C4, G4, A4
        }
        self.current_note = 60

    def get_next_note(self):
        # Seleciona a próxima nota baseada na nota atual
        possible_next = self.transitions.get(self.current_note, [60, 62, 64, 65, 67])
        self.current_note = random.choice(possible_next)
        return self.current_note

    def generate_sequence(self, length=32):
        print(f"Gerando sequência de {length} notas usando Cadeia de Markov...")
        sequence = []
        current_time = 0.0
        
        for _ in range(length):
            pitch = self.get_next_note()
            duration = random.choice([0.25, 0.5, 1.0])
            velocity = random.randint(80, 110)
            
            sequence.append({
                'pitch': pitch,
                'start': current_time,
                'end': current_time + duration,
                'velocity': velocity
            })
            current_time += duration
            
        return sequence

if __name__ == "__main__":
    gen = MarkovMusicGenerator()
    seq = gen.generate_sequence(10)
    for s in seq:
        print(f"Nota: {s['pitch']} das {s['start']} às {s['end']}")
