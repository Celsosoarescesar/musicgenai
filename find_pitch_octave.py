# find_pitch_octave.py
# Dado um inteiro de tom MIDI, encontra sua oitava e o nome da nota.

def find_pitch_octave():
    # Nomes das notas em uma oitava
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Obter entrada do usuário
    try:
        pitch_input = input("Por favor, insira um tom MIDI (0 - 127): ")
        pitch = int(pitch_input)
        
        if not (0 <= pitch <= 127):
            print("Erro: O tom MIDI deve estar entre 0 e 127.")
            return

        # Uma oitava tem 12 tons, e a numeração das oitavas começa em -1.
        # A divisão inteira (//) por 12 e a subtração de 1 nos dá a oitava.
        octave = (pitch // 12) - 1
        
        # Encontrar o nome da nota usando o resto da divisão por 12
        note_name = note_names[pitch % 12]

        # Saída do resultado
        print(f"O tom MIDI {pitch} é a nota {note_name} na oitava {octave}")
        
    except ValueError:
        print("Erro: Por favor, insira um número inteiro válido.")

if __name__ == "__main__":
    find_pitch_octave()
