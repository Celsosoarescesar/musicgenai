try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch não encontrado. Usando modo de simulação.")

if TORCH_AVAILABLE:
    class MusicRNN(nn.Module):
        def __init__(self, input_size=1, hidden_size=64, output_size=128):
            super(MusicRNN, self).__init__()
            self.hidden_size = hidden_size
            self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
            self.fc = nn.Linear(hidden_size, output_size)

        def forward(self, x, hidden=None):
            # x shape: (batch, seq_len, input_size)
            out, hidden = self.lstm(x, hidden)
            # out shape: (batch, seq_len, hidden_size)
            out = self.fc(out[:, -1, :]) # Pega o último output da sequência
            return out, hidden

    def get_model():
        model = MusicRNN()
        return model
else:
    class MusicRNN:
        def __init__(self, *args, **kwargs):
            pass
        def __call__(self, *args, **kwargs):
            return "Simulated Output"

    def get_model():
        return MusicRNN()
