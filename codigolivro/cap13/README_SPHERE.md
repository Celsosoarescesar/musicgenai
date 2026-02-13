# Musical Sphere - REAPER Script

## 📋 Descrição

Este script cria uma composição musical baseada em uma esfera 3D rotativa. Pontos são distribuídos aleatoriamente na superfície da esfera, e quando cada ponto cruza o **meridiano principal** (a linha vertical imaginária mais próxima do observador), uma nota musical é tocada.

A altura da nota (pitch) é determinada pela **latitude** do ponto na esfera:
- **Pontos no polo norte** → Notas agudas
- **Pontos no equador** → Notas médias  
- **Pontos no polo sul** → Notas graves

## 🎵 Conceito Musical

Este é um exemplo de **música generativa espacial**, onde:
- A geometria 3D determina os eventos musicais
- O tempo é determinado pela rotação da esfera
- A altura das notas é mapeada da latitude (ângulo φ - phi)
- Cada ponto cria um padrão rítmico único baseado em sua posição

## 🎯 Mapeamento Esférico → Musical

```
Coordenadas Esféricas:
- r (raio)     → Constante (todos os pontos na superfície)
- θ (theta)    → Rotação/Tempo (quando cruza 0, toca nota)
- φ (phi)      → Latitude/Pitch (0 = agudo, π = grave)

Parâmetros Musicais:
- Cruzamento do meridiano → Trigger de nota
- Latitude (φ)            → Pitch (C2 a C7)
- Aleatório               → Velocity (60-100)
- Constante               → Duração (0.5 beats)
```

## 🚀 Como Usar

### Executar o Script

```powershell
python spreu_reaper.py
```

**Nota:** O REAPER deve estar aberto e o reapy configurado (veja README_BOIDS.md para instruções de configuração).

## ⚙️ Parâmetros Ajustáveis

Edite estas variáveis no início do script:

```python
# Parâmetros musicais
SCALE = [0, 2, 4, 5, 7, 9, 11]  # Escala maior (pode mudar para menor, pentatônica, etc.)
LOW_PITCH = 36   # C2 - nota mais grave
HIGH_PITCH = 96  # C7 - nota mais aguda
NOTE_DURATION = 0.5  # Duração de cada nota em beats

# Parâmetros da esfera
RADIUS = 200         # Raio da esfera (não afeta música, apenas simulação)
NUM_POINTS = 200     # Número de pontos na esfera (mais pontos = mais notas)
VELOCITY = 0.01      # Velocidade angular (maior = rotação mais rápida)
NUM_FRAMES = 1000    # Quantos frames simular (duração da composição)
TIME_SCALE = 0.05    # Conversão frame → beats (menor = mais lento)
```

## 🎼 Resultado Esperado

Com os parâmetros padrão:
- **Track:** "Musical Sphere"
- **Duração:** ~50 beats (NUM_FRAMES × TIME_SCALE)
- **Notas:** Variável (depende de quantas vezes pontos cruzam o meridiano)
- **Escala:** Dó maior (C major)
- **Registro:** C2 a C7 (5 oitavas)

## 💡 Experimentos Criativos

### 1. **Esfera Lenta e Esparsa**
```python
NUM_POINTS = 50      # Menos pontos
VELOCITY = 0.005     # Rotação mais lenta
TIME_SCALE = 0.1     # Tempo mais espaçado
NOTE_DURATION = 2.0  # Notas longas
```
**Resultado:** Composição ambient esparsa e contemplativa

### 2. **Esfera Rápida e Densa**
```python
NUM_POINTS = 500     # Muitos pontos
VELOCITY = 0.05      # Rotação rápida
TIME_SCALE = 0.02    # Tempo comprimido
NOTE_DURATION = 0.25 # Notas curtas
```
**Resultado:** Textura densa e rítmica

### 3. **Escala Pentatônica Menor**
```python
SCALE = [0, 3, 5, 7, 10]  # Pentatônica menor
LOW_PITCH = 48            # C3
HIGH_PITCH = 72           # C5
```
**Resultado:** Som mais oriental/meditativo

### 4. **Escala Cromática (Todas as notas)**
```python
SCALE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # Cromática
```
**Resultado:** Som mais dissonante e experimental

### 5. **Apenas Oitavas**
```python
SCALE = [0]  # Apenas a tônica
```
**Resultado:** Padrão rítmico puro sem variação melódica

## 🎨 Visualização Mental

Imagine a esfera girando:
```
        ╱─────╲
      ╱    •    ╲     ← Polo Norte (notas agudas)
     │  •     •  │
     │ •   ║   • │    ← Meridiano principal (linha de trigger)
     │  •  ║  •  │
      ╲   •║•   ╱     ← Equador (notas médias)
        ╲─────╱
           •          ← Polo Sul (notas graves)
```

Quando um ponto `•` cruza a linha `║` (meridiano), uma nota é tocada!

## 🔬 Matemática por Trás

### Coordenadas Esféricas
```
x = r × sin(φ) × cos(θ + π/2)
y = r × cos(φ)
z = r × sin(φ) × sin(θ + π/2)
```

### Detecção de Cruzamento
```python
if old_theta > new_theta:  # Cruzou de 2π para 0
    # Toca nota!
```

### Mapeamento de Pitch
```python
pitch = map_to_scale(φ, 0, π, LOW_PITCH, HIGH_PITCH, SCALE)
```

## 📊 Análise de Frequência de Notas

Com distribuição uniforme de pontos:
- **Mais notas no equador** (maior circunferência)
- **Menos notas nos polos** (menor circunferência)
- Resultado: Registro médio mais denso que extremos

## 🐛 Solução de Problemas

### Poucas notas geradas
- Aumente `NUM_POINTS` (mais pontos)
- Aumente `NUM_FRAMES` (mais tempo de simulação)
- Aumente `VELOCITY` (rotação mais rápida)

### Muitas notas (muito denso)
- Diminua `NUM_POINTS`
- Diminua `VELOCITY`
- Aumente `TIME_SCALE` (espaça mais as notas no tempo)

### Notas fora da escala
- Verifique a definição de `SCALE`
- Ajuste `LOW_PITCH` e `HIGH_PITCH`

## 📚 Referências

- [Spherical Coordinate System](http://en.wikipedia.org/wiki/Spherical_coordinate_system)
- [Generative Music](https://en.wikipedia.org/wiki/Generative_music)
- [reapy Documentation](https://python-reapy.readthedocs.io/)

## 🎭 Inspiração

Este código é baseado em trabalho de **Uri Wilensky (1998)**, distribuído com NetLogo sob Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.

A ideia de mapear geometria espacial para música tem raízes em:
- **Música das Esferas** (Pitágoras)
- **Música Estocástica** (Iannis Xenakis)
- **Música Generativa** (Brian Eno)
