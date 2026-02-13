import reapy
from magenta_generator import generate_melody
from reaper_integration import create_magenta_track

def run_project():
    print("Iniciando Projeto REAPER + Magenta...")
    
    try:
        # 1. Conecta ao Projeto REAPER
        project = reapy.Project()
        project.bpm = 120
        
        # 2. Gera a melodia (Estilo Magenta)
        # Podemos gerar várias partes
        melody_main = generate_melody(length=24, scale=[60, 62, 64, 67, 69]) # Pentatônica Maior
        melody_bass = generate_melody(length=8, scale=[36, 38, 40, 43])    # Escala grave
        
        # 3. Integra no REAPER
        create_magenta_track(project, melody_main, "Magenta Lead")
        create_magenta_track(project, melody_bass, "Magenta Bass")
        
        print("\nSucesso! Verifique seu REAPER.")
        
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Certifique-se de que o REAPER está aberto e o 'reapy-server' está rodando.")

if __name__ == "__main__":
    run_project()
