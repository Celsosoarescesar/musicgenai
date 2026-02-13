import reapy
from torch_generator import generate_torch_melody
from reaper_integration import create_torch_track

def run_torch_project():
    print("--- REAPER + PyTorch Integration ---")
    
    try:
        # 1. Conecta ao REAPER
        project = reapy.Project()
        
        # 2. Gera melodia via PyTorch Model
        melody = generate_torch_melody(num_notes=32)
        
        # 3. Cria pista no REAPER
        create_torch_track(project, melody, "PyTorch LSTM Lead")
        
        print("\nProjeto finalizado! Confira o REAPER.")
        
    except Exception as e:
        print(f"\nErro: {e}")
        print("Certifique-se de que o REAPER está aberto.")

if __name__ == "__main__":
    run_torch_project()
