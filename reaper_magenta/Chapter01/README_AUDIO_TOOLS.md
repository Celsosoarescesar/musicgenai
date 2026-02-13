# Audio Analysis & Conversion Tools for REAPER

## 📋 Descrição

Ferramentas para análise de áudio e conversão para MIDI no REAPER. Portado do script original `wav2plot.py` com funcionalidades expandidas.

## 🎵 Scripts Disponíveis

### 1. **wav2plot_reaper.py** - Análise e Visualização de Áudio

Analisa arquivos WAV e cria visualizações de forma de onda.

**Funcionalidades:**
- ✅ Plotar formas de onda de arquivos WAV
- ✅ Analisar amplitude, RMS, e características espectrais
- ✅ Importar e analisar áudio de projetos REAPER
- ✅ Gerar relatórios visuais salvos como PNG

**Uso:**

```bash
# Analisar arquivo WAV externo
python wav2plot_reaper.py audio.wav

# Analisar múltiplos arquivos
python wav2plot_reaper.py audio1.wav audio2.wav audio3.wav

# Analisar todos os itens de áudio no projeto REAPER
python wav2plot_reaper.py --reaper

# Analisar apenas uma track específica
python wav2plot_reaper.py --reaper "Drums"

# Importar WAV para REAPER e analisar
python wav2plot_reaper.py --import audio.wav
```

**Saída:**
- Gráficos de forma de onda (exibidos e salvos como PNG)
- Relatório com estatísticas:
  - Duração
  - Taxa de amostragem
  - Número de canais
  - Amplitude máxima
  - RMS por canal
  - Posições de picos

---

### 2. **wav2midi_reaper.py** - Conversão de Áudio para MIDI

Detecta transientes (onsets) em áudio e converte para notas MIDI.

**Funcionalidades:**
- ✅ Detecção automática de onsets/transientes
- ✅ Conversão de amplitude para velocity MIDI
- ✅ Modo melódico (pitch varia com posição)
- ✅ Modo rítmico (pitch fixo, ideal para drums)
- ✅ Criação automática de tracks MIDI no REAPER

**Uso:**

```bash
# Modo padrão (melódico)
python wav2midi_reaper.py audio.wav

# Modo rítmico (todos os hits no mesmo pitch)
python wav2midi_reaper.py --rhythm drums.wav

# Modo rítmico com pitch customizado (36 = Kick drum GM)
python wav2midi_reaper.py --rhythm drums.wav 36

# Modo melódico com parâmetros customizados
python wav2midi_reaper.py --melody vocal.wav 60 24
#                                            ^   ^
#                                    base_pitch  range
```

**Parâmetros:**
- `base_pitch`: Nota MIDI base (padrão: 60 = C4)
- `pitch_range`: Alcance de semitons (padrão: 12 = 1 oitava)
- `drum_pitch`: Pitch para modo rítmico (padrão: 36 = Kick)

---

## 🎯 Casos de Uso

### 1. **Análise de Mixagem**
```bash
# Analisar todas as tracks do projeto
python wav2plot_reaper.py --reaper

# Comparar formas de onda
python wav2plot_reaper.py mix_v1.wav mix_v2.wav mix_final.wav
```

### 2. **Extração de Ritmo de Drums**
```bash
# Converter drum loop para MIDI
python wav2midi_reaper.py --rhythm drum_loop.wav 36

# Resultado: Track MIDI com hits detectados
# Útil para: triggering samples, análise rítmica, quantização
```

### 3. **Criação de Melodia a Partir de Áudio**
```bash
# Converter vocal/melodia para MIDI
python wav2midi_reaper.py --melody vocal.wav 60 12

# Resultado: Contorno melódico baseado em transientes
# Útil para: harmonização, análise melódica, MIDI mockups
```

### 4. **Análise de Dinâmica**
```bash
# Importar e analisar arquivo
python wav2plot_reaper.py --import performance.wav

# Resultado: Visualização + estatísticas de amplitude
# Útil para: análise de dinâmica, compressão, masterização
```

---

## 🔧 Detecção de Onsets

O algoritmo de detecção de onsets funciona assim:

```python
1. Calcular envelope (amplitude absoluta)
2. Suavizar com janela de 10ms
3. Calcular diferença (onset strength)
4. Detectar picos acima do threshold
5. Aplicar distância mínima entre onsets
```

**Parâmetros ajustáveis** (edite no código):

```python
threshold = 0.3      # Sensibilidade (0-1, menor = mais sensível)
min_distance = 0.05  # Distância mínima entre onsets (segundos)
```

---

## 📊 Mapeamentos

### Áudio → MIDI (wav2midi_reaper.py)

| **Característica de Áudio** | **Parâmetro MIDI** |
|---|---|
| Onset/Transiente | Trigger de nota |
| Amplitude no onset | Velocity (40-127) |
| Posição temporal | Start time |
| Tempo até próximo onset | Duration |
| Índice do onset | Pitch offset (modo melódico) |

### Exemplo de Conversão

```
Áudio:  |----▲--------▲--▲----------▲----|
        0s   0.5s    1s  1.2s      2s

MIDI:   Note(pitch=60, vel=80, start=0.5, end=1.0)
        Note(pitch=61, vel=100, start=1.0, end=1.2)
        Note(pitch=62, vel=60, start=1.2, end=1.7)
        Note(pitch=63, vel=90, start=2.0, end=2.1)
```

---

## 🎨 Visualizações

### wav2plot_reaper.py gera:

```
┌─────────────────────────────────────────────┐
│ audio.wav - Channel 1                       │
│                                             │
│     ╱╲        ╱╲                           │
│    ╱  ╲      ╱  ╲      ╱╲                  │
│───╱────╲────╱────╲────╱──╲─────────────── │
│         ╲  ╱      ╲  ╱    ╲                │
│          ╲╱        ╲╱                       │
│                                             │
│ Time (s) ──────────────────────────────────▶│
└─────────────────────────────────────────────┘
```

Salvo como: `audio.png`

---

## 🐛 Solução de Problemas

### "No notes detected!"
- Áudio muito silencioso ou sem transientes claros
- Reduza `threshold` no código (linha ~35 em wav2midi_reaper.py)
- Aumente o volume do áudio antes de processar

### "File not found"
- Verifique o caminho do arquivo
- Use caminhos absolutos se necessário
- Certifique-se de que o arquivo é WAV válido

### Muitos onsets detectados
- Aumente `threshold` (menos sensível)
- Aumente `min_distance` (mais espaçamento)

### Poucos onsets detectados
- Diminua `threshold` (mais sensível)
- Diminua `min_distance` (menos espaçamento)

---

## 💡 Experimentos Criativos

### 1. **Drum Replacement**
```bash
# Detectar hits de bateria e criar MIDI
python wav2midi_reaper.py --rhythm acoustic_drums.wav 36

# No REAPER:
# 1. Adicione sampler na track MIDI
# 2. Carregue samples de bateria
# 3. Ajuste velocities se necessário
```

### 2. **Análise Comparativa**
```bash
# Comparar versões de mix
python wav2plot_reaper.py mix_rough.wav mix_final.wav

# Observe diferenças em:
# - Amplitude máxima (loudness)
# - RMS (densidade/compressão)
# - Forma de onda (dinâmica)
```

### 3. **Melodia Generativa**
```bash
# Criar melodia a partir de percussão
python wav2midi_reaper.py --melody shaker.wav 72 24

# Resultado: Melodia aleatória mas ritmicamente coerente
# Útil para: inspiração, happy accidents, texturas
```

### 4. **Quantização Humanizada**
```bash
# Extrair timing de performance humana
python wav2midi_reaper.py --rhythm human_claps.wav 60

# Use o MIDI resultante como groove template
```

---

## 📚 Dependências

```bash
pip install numpy matplotlib reapy wave
```

**Nota:** `wave` faz parte da biblioteca padrão do Python.

---

## 🔄 Diferenças do Original

| **Original (wav2plot.py)** | **REAPER Version** |
|---|---|
| Apenas visualização | Visualização + MIDI |
| Análise offline | Integração com REAPER |
| Plots interativos | Plots salvos + relatórios |
| Sem detecção de onsets | Detecção automática |
| Sem saída MIDI | Criação de tracks MIDI |

---

## 🎓 Conceitos Musicais

### Onset Detection
**Onset** = Início de um evento sonoro (nota, hit, transiente)

Aplicações:
- Análise rítmica
- Beat tracking
- Segmentação de áudio
- Sincronização áudio-MIDI

### Envelope
**Envelope** = Contorno de amplitude ao longo do tempo

Usado para:
- Detectar ataques (onsets)
- Análise de dinâmica
- Compressão/expansão
- Síntese (ADSR)

---

## 📖 Referências

- [Onset Detection Algorithms](https://en.wikipedia.org/wiki/Onset_detection)
- [Audio Signal Processing](https://en.wikipedia.org/wiki/Audio_signal_processing)
- [reapy Documentation](https://python-reapy.readthedocs.io/)
- [MIDI Specification](https://www.midi.org/specifications)

---

## ✨ Próximas Melhorias Possíveis

- [ ] Detecção de pitch (audio-to-MIDI melódico real)
- [ ] Análise espectral (FFT)
- [ ] Detecção de tempo/BPM
- [ ] Quantização automática
- [ ] Suporte para múltiplos formatos (MP3, FLAC, etc.)
- [ ] Interface gráfica (GUI)
- [ ] Batch processing
- [ ] Machine learning para melhor detecção
