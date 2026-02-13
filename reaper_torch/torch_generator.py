import random
from torch_model import TORCH_AVAILABLE, get_model

if TORCH_AVAILABLE:
    import torch

def generate_torch_melody(num_notes=16):
    print(f"Gerando melodia com {'PyTorch' if TORCH_AVAILABLE else 'Simulação'}...")
    
    model = get_model()
    melody = []
    current_time = 0.0
    
    # Se tiver torch, faríamos inferência real aqui
    # Por agora, usaremos a estrutura mas com valores controlados
    
    for i in range(num_notes):
        if TORCH_AVAILABLE:
            # Simulação de input para o modelo
            dummy_input = torch.randn(1, 1, 1) 
            # output, _ = model(dummy_input)
            # pitch = torch.argmax(output).item()
            pitch = 60 + random.randint(0, 12) # Simplificado
        else:
            pitch = 60 + random.randint(0, 12)
            
        duration = 0.5
        velocity = 80 + random.randint(0, 20)
        
        melody.append({
            'start': current_time,
            'end': current_time + duration,
            'pitch': pitch,
            'velocity': velocity
        })
        current_time += duration
        
    return melody

if __name__ == "__main__":
    m = generate_torch_melody()
    print(f"Geradas {len(m)} notas.")
