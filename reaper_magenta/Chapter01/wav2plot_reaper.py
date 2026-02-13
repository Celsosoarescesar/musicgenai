"""
wav2plot_reaper.py

Analyzes audio files from REAPER project and creates visualizations.
Can also analyze external WAV files and import them into REAPER.

Features:
- Plot waveforms from REAPER items or external WAV files
- Analyze amplitude, frequency, and spectral content
- Import analyzed audio into REAPER project
- Generate visual reports of audio characteristics
"""

import sys
import wave
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import reapy


def plot_wav(file_path, show_plot=True, save_plot=False):
    """
    Plot waveform from a WAV file.
    
    Args:
        file_path: Path to WAV file
        show_plot: Whether to display the plot
        save_plot: Whether to save the plot to file
    
    Returns:
        Dictionary with audio analysis data
    """
    print(f"Analyzing: {file_path}")
    
    with wave.open(str(file_path), 'r') as wav_file:
        # Extract Raw Audio from Wav File
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        
        # Get audio parameters
        num_channels = wav_file.getnchannels()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        duration = num_frames / frame_rate
        
        # Split the data into channels
        channels = [[] for _ in range(num_channels)]
        for index, datum in enumerate(signal):
            channels[index % num_channels].append(datum)
        
        # Convert to numpy arrays
        channels = [np.array(ch) for ch in channels]
        
        # Get time from indices
        time = np.linspace(0, duration, num=len(channels[0]))
        
        # Calculate statistics
        analysis = {
            'file': file_path,
            'duration': duration,
            'sample_rate': frame_rate,
            'num_channels': num_channels,
            'num_frames': num_frames,
            'max_amplitude': max([np.max(np.abs(ch)) for ch in channels]),
            'rms': [np.sqrt(np.mean(ch**2)) for ch in channels],
            'peak_positions': [time[np.argmax(np.abs(ch))] for ch in channels]
        }
        
        # Plot
        if show_plot or save_plot:
            plt.figure(num=None, figsize=(16, 6), dpi=80, facecolor='w', edgecolor='k')
            
            for i, channel in enumerate(channels):
                plt.subplot(num_channels, 1, i + 1)
                plt.plot(time, channel, linewidth=0.5)
                plt.ylabel(f'Channel {i + 1}')
                plt.xlabel('Time (s)')
                plt.title(f'{Path(file_path).name} - Channel {i + 1}')
                plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_plot:
                plot_path = Path(file_path).with_suffix('.png')
                plt.savefig(plot_path)
                print(f"Plot saved to: {plot_path}")
            
            if show_plot:
                plt.show()
            else:
                plt.close()
        
        return analysis


def analyze_reaper_items(track_name=None):
    """
    Analyze audio items from REAPER project.
    
    Args:
        track_name: Optional track name to filter. If None, analyzes all tracks.
    
    Returns:
        List of analysis results for each audio item
    """
    project = reapy.Project()
    results = []
    
    tracks = project.tracks
    if track_name:
        tracks = [t for t in tracks if t.name == track_name]
    
    for track in tracks:
        print(f"\nAnalyzing track: {track.name}")
        
        for item in track.items:
            # Get the active take
            take = item.active_take
            if not take:
                continue
            
            # Get the source file
            source = take.source
            if not source:
                continue
            
            # Get file path
            file_path = source.filename
            
            if file_path and os.path.exists(file_path):
                analysis = plot_wav(file_path, show_plot=False, save_plot=True)
                analysis['track'] = track.name
                analysis['item_position'] = item.position
                analysis['item_length'] = item.length
                results.append(analysis)
    
    return results


def import_wav_to_reaper(wav_file, track_name="Audio Analysis", position=0):
    """
    Import a WAV file into REAPER and analyze it.
    
    Args:
        wav_file: Path to WAV file
        track_name: Name for the track
        position: Position in timeline (seconds)
    
    Returns:
        Analysis results
    """
    project = reapy.Project()
    
    # Create or get track
    track = None
    for t in project.tracks:
        if t.name == track_name:
            track = t
            break
    
    if not track:
        track = project.add_track(name=track_name)
    
    # Add media item
    item = track.add_media_item(wav_file, position=position)
    
    print(f"Imported {wav_file} to track '{track_name}' at position {position}s")
    
    # Analyze the file
    analysis = plot_wav(wav_file, show_plot=True, save_plot=True)
    
    return analysis


def print_analysis_report(analysis_list):
    """Print a formatted report of audio analysis."""
    print("\n" + "=" * 80)
    print("AUDIO ANALYSIS REPORT")
    print("=" * 80)
    
    for i, analysis in enumerate(analysis_list, 1):
        print(f"\n[{i}] {Path(analysis['file']).name}")
        print(f"    Duration: {analysis['duration']:.2f}s")
        print(f"    Sample Rate: {analysis['sample_rate']} Hz")
        print(f"    Channels: {analysis['num_channels']}")
        print(f"    Max Amplitude: {analysis['max_amplitude']}")
        print(f"    RMS: {[f'{rms:.2f}' for rms in analysis['rms']]}")
        
        if 'track' in analysis:
            print(f"    Track: {analysis['track']}")
            print(f"    Position: {analysis['item_position']:.2f}s")
            print(f"    Length: {analysis['item_length']:.2f}s")
    
    print("\n" + "=" * 80)


def main():
    """Main function with command-line interface."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python wav2plot_reaper.py <wav_file> [wav_file2 ...]  # Analyze WAV files")
        print("  python wav2plot_reaper.py --reaper [track_name]       # Analyze REAPER project")
        print("  python wav2plot_reaper.py --import <wav_file>         # Import to REAPER")
        return
    
    # Check for special modes
    if sys.argv[1] == "--reaper":
        # Analyze REAPER project
        track_name = sys.argv[2] if len(sys.argv) > 2 else None
        results = analyze_reaper_items(track_name)
        print_analysis_report(results)
    
    elif sys.argv[1] == "--import":
        # Import files to REAPER
        for wav_file in sys.argv[2:]:
            if os.path.exists(wav_file):
                import_wav_to_reaper(wav_file)
            else:
                print(f"File not found: {wav_file}")
    
    else:
        # Analyze WAV files
        results = []
        for wav_file in sys.argv[1:]:
            if os.path.exists(wav_file):
                analysis = plot_wav(wav_file, show_plot=True, save_plot=True)
                results.append(analysis)
            else:
                print(f"File not found: {wav_file}")
        
        if results:
            print_analysis_report(results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
