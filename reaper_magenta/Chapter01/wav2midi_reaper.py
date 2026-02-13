"""
wav2midi_reaper.py

Advanced audio analysis tool that converts audio characteristics to MIDI.
Analyzes amplitude envelope and creates MIDI notes based on audio features.

This is useful for:
- Creating rhythmic MIDI from drum loops
- Extracting amplitude envelope as MIDI velocity
- Generating MIDI triggers from audio transients
"""

import sys
import wave
import os
from pathlib import Path

import numpy as np
import reapy


def detect_onsets(audio_data, sample_rate, threshold=0.3, min_distance=0.05):
    """
    Detect onset times in audio signal.
    
    Args:
        audio_data: Audio samples (numpy array)
        sample_rate: Sample rate in Hz
        threshold: Onset detection threshold (0-1)
        min_distance: Minimum time between onsets in seconds
    
    Returns:
        List of onset times in seconds
    """
    # Calculate envelope (absolute value with smoothing)
    envelope = np.abs(audio_data)
    
    # Smooth the envelope
    window_size = int(sample_rate * 0.01)  # 10ms window
    envelope = np.convolve(envelope, np.ones(window_size)/window_size, mode='same')
    
    # Calculate difference (onset strength)
    diff = np.diff(envelope)
    diff = np.maximum(diff, 0)  # Only positive changes
    
    # Normalize
    if np.max(diff) > 0:
        diff = diff / np.max(diff)
    
    # Find peaks above threshold
    onsets = []
    min_samples = int(min_distance * sample_rate)
    last_onset = -min_samples
    
    for i, value in enumerate(diff):
        if value > threshold and (i - last_onset) > min_samples:
            onsets.append(i / sample_rate)
            last_onset = i
    
    return onsets


def analyze_wav_for_midi(file_path, base_pitch=60, pitch_range=12):
    """
    Analyze WAV file and extract MIDI-compatible data.
    
    Args:
        file_path: Path to WAV file
        base_pitch: Base MIDI pitch (default: C4 = 60)
        pitch_range: Range of pitches to use (in semitones)
    
    Returns:
        Dictionary with MIDI note data
    """
    print(f"Analyzing {file_path} for MIDI conversion...")
    
    with wave.open(str(file_path), 'r') as wav_file:
        # Extract audio
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        
        # Get parameters
        num_channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        duration = len(signal) / num_channels / sample_rate
        
        # Mix to mono if stereo
        if num_channels > 1:
            signal = signal.reshape(-1, num_channels)
            signal = np.mean(signal, axis=1)
        
        # Normalize
        signal = signal.astype(np.float32)
        if np.max(np.abs(signal)) > 0:
            signal = signal / np.max(np.abs(signal))
        
        # Detect onsets
        onsets = detect_onsets(signal, sample_rate, threshold=0.3, min_distance=0.05)
        
        # Create MIDI notes from onsets
        notes = []
        for i, onset_time in enumerate(onsets):
            # Calculate amplitude at onset
            sample_idx = int(onset_time * sample_rate)
            if sample_idx < len(signal):
                amplitude = abs(signal[sample_idx])
            else:
                amplitude = 0.5
            
            # Map amplitude to velocity
            velocity = int(np.clip(amplitude * 127, 40, 127))
            
            # Map position to pitch (creates melodic contour)
            pitch_offset = int((i % pitch_range))
            pitch = base_pitch + pitch_offset
            
            # Note duration (until next onset or 0.1s)
            if i < len(onsets) - 1:
                duration = min(onsets[i + 1] - onset_time, 0.5)
            else:
                duration = 0.1
            
            notes.append({
                'pitch': pitch,
                'start': onset_time,
                'end': onset_time + duration,
                'velocity': velocity
            })
        
        print(f"Detected {len(notes)} onsets/notes")
        
        return {
            'file': file_path,
            'duration': duration,
            'sample_rate': sample_rate,
            'notes': notes
        }


def create_midi_from_audio(wav_file, track_name="Audio to MIDI", 
                           base_pitch=60, pitch_range=12):
    """
    Analyze audio file and create MIDI track in REAPER.
    
    Args:
        wav_file: Path to WAV file
        track_name: Name for MIDI track
        base_pitch: Base MIDI pitch
        pitch_range: Range of pitches
    
    Returns:
        Analysis results
    """
    # Analyze audio
    analysis = analyze_wav_for_midi(wav_file, base_pitch, pitch_range)
    
    if not analysis['notes']:
        print("No notes detected!")
        return analysis
    
    # Connect to REAPER
    print("Creating MIDI track in REAPER...")
    project = reapy.Project()
    
    # Create MIDI track
    track = project.add_track(name=track_name)
    
    # Calculate total duration
    total_duration = analysis['duration']
    
    # Create MIDI item
    item = track.add_midi_item(start=0, end=total_duration)
    take = item.active_take
    
    # Add notes
    for note in analysis['notes']:
        take.add_note(
            pitch=note['pitch'],
            start=note['start'],
            end=note['end'],
            velocity=note['velocity']
        )
    
    print(f"✓ Created MIDI track with {len(analysis['notes'])} notes")
    
    return analysis


def create_rhythm_from_audio(wav_file, track_name="Audio Rhythm", 
                             drum_pitch=36):
    """
    Create rhythmic MIDI pattern from audio transients.
    All notes use the same pitch (useful for drum mapping).
    
    Args:
        wav_file: Path to WAV file
        track_name: Name for MIDI track
        drum_pitch: MIDI pitch to use (e.g., 36 = Kick drum in GM)
    """
    # Analyze with single pitch
    analysis = analyze_wav_for_midi(wav_file, base_pitch=drum_pitch, pitch_range=1)
    
    if not analysis['notes']:
        print("No rhythm detected!")
        return analysis
    
    # Connect to REAPER
    print("Creating rhythm track in REAPER...")
    project = reapy.Project()
    
    # Create MIDI track
    track = project.add_track(name=track_name)
    
    # Create MIDI item
    total_duration = analysis['duration']
    item = track.add_midi_item(start=0, end=total_duration)
    take = item.active_take
    
    # Add notes (all same pitch, varying velocity)
    for note in analysis['notes']:
        take.add_note(
            pitch=drum_pitch,
            start=note['start'],
            end=note['end'],
            velocity=note['velocity']
        )
    
    print(f"✓ Created rhythm track with {len(analysis['notes'])} hits")
    
    return analysis


def main():
    """Main function with command-line interface."""
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("WAV to MIDI Converter for REAPER")
        print("=" * 70)
        print("\nUsage:")
        print("  # Convert audio to melodic MIDI:")
        print("  python wav2midi_reaper.py <wav_file>")
        print()
        print("  # Convert audio to rhythm (single pitch):")
        print("  python wav2midi_reaper.py --rhythm <wav_file> [pitch]")
        print()
        print("  # Custom pitch range:")
        print("  python wav2midi_reaper.py --melody <wav_file> <base_pitch> <range>")
        print()
        print("Examples:")
        print("  python wav2midi_reaper.py drums.wav")
        print("  python wav2midi_reaper.py --rhythm drums.wav 36")
        print("  python wav2midi_reaper.py --melody vocal.wav 60 24")
        print("=" * 70)
        return
    
    try:
        if sys.argv[1] == "--rhythm":
            # Rhythm mode
            wav_file = sys.argv[2]
            drum_pitch = int(sys.argv[3]) if len(sys.argv) > 3 else 36
            
            if os.path.exists(wav_file):
                create_rhythm_from_audio(wav_file, drum_pitch=drum_pitch)
            else:
                print(f"File not found: {wav_file}")
        
        elif sys.argv[1] == "--melody":
            # Melody mode with custom parameters
            wav_file = sys.argv[2]
            base_pitch = int(sys.argv[3]) if len(sys.argv) > 3 else 60
            pitch_range = int(sys.argv[4]) if len(sys.argv) > 4 else 12
            
            if os.path.exists(wav_file):
                create_midi_from_audio(wav_file, base_pitch=base_pitch, 
                                      pitch_range=pitch_range)
            else:
                print(f"File not found: {wav_file}")
        
        else:
            # Default mode
            wav_file = sys.argv[1]
            
            if os.path.exists(wav_file):
                create_midi_from_audio(wav_file)
            else:
                print(f"File not found: {wav_file}")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
