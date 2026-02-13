import reapy
from markov_gen import MarkovMusicGenerator
from reaper_integration import create_markov_track

def run_algorithmic_project():
    print("--- REAPER + Markov Algorithmic Music ---")
    
    try:
        # 1. Conecta ao REAPER
        project = reapy.Project()
        project.bpm = 100
        
        # 2. Gera música usando Cadeia de Markov
        gen = MarkovMusicGenerator()
        melodia_1 = gen.generate_sequence(length=40)
        
        # Gera uma segunda voz variada (resetando ou pegando novo estado)
        melodia_2 = gen.generate_sequence(length=20)
        
        # 3. Importa para o REAPER
        create_markov_track(project, melodia_1, "Markov Lead")
        create_markov_track(project, melodia_2, "Markov Harmony")
        
        print("\nSucesso! Abra o REAPER para ouvir o resultado estocástico.")
        
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Verifique se o REAPER está aberto e o reapy-server configurado.")

if __name__ == "__main__":
    run_algorithmic_project()
