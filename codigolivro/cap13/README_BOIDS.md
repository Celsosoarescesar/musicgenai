# Boids Flocking Music - REAPER Script

## 📋 Descrição

Este script transforma a simulação de comportamento de boids (flocking behavior) em música no REAPER. Os boids seguem três regras simples que geram padrões complexos e emergentes:

1. **Separação** - Evitar colisões com outros boids
2. **Alinhamento** - Seguir a direção do grupo local
3. **Coesão** - Mover-se em direção ao centro do universo

## 🎵 Mapeamento Visual → Musical

- **Posição X** → **Tempo** (posição temporal das notas em beats)
- **Posição Y** → **Pitch** (altura das notas MIDI, 0-127)
- **Velocidade do boid** → **Velocity MIDI** (intensidade/volume da nota)

## 🚀 Como Usar

### Opção 1: Executar de Fora do REAPER (Requer Configuração)

1. **Abra o REAPER**

2. **Configure o reapy** (apenas primeira vez):
   - No REAPER, vá em `Actions` → `Show action list`
   - Procure por "ReaScript: Run Python script"
   - Execute este código Python uma vez dentro do REAPER:
   ```python
   import reapy
   reapy.config.enable_dist_api()
   ```

3. **Execute o script**:
   ```powershell
   python boids_reaper.py
   ```

### Opção 2: Executar Dentro do REAPER (Mais Simples)

1. **Abra o REAPER**

2. **Carregue o script**:
   - `Actions` → `Show action list` → `ReaScript: Load`
   - Selecione `boids_reaper.py`

3. **Execute**:
   - O script aparecerá na lista de actions
   - Clique em "Run" ou atribua um atalho de teclado

## ⚙️ Parâmetros Ajustáveis

Edite estas variáveis no início do script para personalizar a música:

```python
# Parâmetros do universo
universeWidth = 1000   # Alcance temporal (em beats)
universeHeight = 127   # Alcance de pitch MIDI (0-127)

# Parâmetros de geração
numBoids = 50          # Número de vozes musicais
numFrames = 100        # Duração da composição (frames)

# Parâmetros musicais
noteLength = 0.25      # Duração de cada nota em beats
timeScale = 0.1        # Escala temporal (frame → beats)
pitchOffset = 36       # Transpor para registro musical (C2 = 36)

# Comportamento dos boids
minSeparation = 10     # Distância mínima entre boids
flockThreshold = 30    # Distância para considerar "grupo local"
separationFactor = 0.01   # Força de separação
alignmentFactor = 0.16    # Força de alinhamento
cohesionFactor = 0.01     # Força de coesão
frictionFactor = 1.1      # Resistência ao movimento
```

## 🎼 Resultado Esperado

O script criará:
- **1 track MIDI** chamada "Boid Flocking"
- **1 MIDI item** contendo todas as notas
- **Padrões musicais emergentes** baseados no comportamento dos boids

Com `numBoids=50` e `numFrames=100`, você terá aproximadamente **5000 notas** criando texturas musicais complexas e orgânicas.

## 🐛 Solução de Problemas

### "Can't reach distant API"
- Certifique-se de que o REAPER está aberto
- Execute `reapy.config.enable_dist_api()` dentro do REAPER

### "AttributeError: 'NoneType' object has no attribute 'request'"
- O REAPER não está rodando ou o reapy não está configurado
- Use a Opção 2 (executar dentro do REAPER)

### Script trava em "Connecting to REAPER..."
- O REAPER não está aberto
- Use Ctrl+C para cancelar e abra o REAPER primeiro

## 💡 Dicas Criativas

1. **Experimente diferentes escalas**:
   - Reduza `universeHeight` para 12 e use `pitchOffset` para criar melodias em uma oitava
   
2. **Crie texturas longas**:
   - Aumente `numFrames` para 500+ e `timeScale` para 0.5
   
3. **Mais vozes, mais densidade**:
   - Aumente `numBoids` para 100-200 para texturas mais densas
   
4. **Notas mais longas**:
   - Aumente `noteLength` para 1.0 ou 2.0 para pads sustentados

5. **Comportamento mais caótico**:
   - Reduza `alignmentFactor` e aumente `separationFactor`

## 📚 Referências

- [Boids Algorithm](http://www.red3d.com/cwr/boids/)
- [Boids Pseudocode](http://www.vergenet.net/~conrad/boids/pseudocode.html)
- [reapy Documentation](https://python-reapy.readthedocs.io/)
