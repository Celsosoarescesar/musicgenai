"""
reapy_zipfMetrics.py

Demonstrates how to calculate Zipf metrics from MIDI files (or selected items)
for comparative analysis. It calculates Zipf slopes and R^2 values
for pitch distribution.

Top-down design:
1. main() -> Orchestrates analysis
2. analyze_item() -> Counts pitches in a REAPER item
3. count_pitches() -> Returns histogram
4. calculate_zipf() -> Performs regression

Ported from zipfMetrics.py
"""

import reapy
import math
import os

# --- Mathematical Functions (Pure Python to avoid external dependencies) ---

def mean(values):
    return sum(values) / len(values)

def linear_regression(x, y):
    """
    Calculates the least squares regression line y = mx + b.
    Returns (slope, r_squared, y_intercept).
    """
    n = len(x)
    if n != len(y) or n == 0:
        return 0, 0, 0
    
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y2 = sum(yi ** 2 for yi in y)
    
    # Calculate Slope (m)
    # m = (N * sum(xy) - sum(x) * sum(y)) / (N * sum(x^2) - (sum(x))^2)
    numerator = (n * sum_xy) - (sum_x * sum_y)
    denominator = (n * sum_x2) - (sum_x ** 2)
    
    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator
        
    # Calculate Intercept (b)
    # b = (sum(y) - m * sum(x)) / N
    intercept = (sum_y - slope * sum_x) / n
    
    # Calculate R-squared
    # r = (N * sum(xy) - sum(x)sum(y)) / sqrt( [N*sum(x^2)-(sum(x))^2] * [N*sum(y^2)-(sum(y))^2] )
    numerator_r = (n * sum_xy) - (sum_x * sum_y)
    denom_r_x = (n * sum_x2) - (sum_x ** 2)
    denom_r_y = (n * sum_y2) - (sum_y ** 2)
    
    if denom_r_x * denom_r_y == 0:
        r_squared = 0
    else:
        r = numerator_r / math.sqrt(denom_r_x * denom_r_y)
        r_squared = r ** 2
        
    return slope, r_squared, intercept

# --- Zipf Analysis ---

def calculate_zipf(histogram):
    """
    Calculates Zipf slope and R^2 from a histogram of pitch counts.
    X = Log(Rank)
    Y = Log(Frequency)
    """
    # Sort counts descending
    counts = sorted(histogram.values(), reverse=True)
    
    if not counts:
        return 0, 0, 0
    
    # Calculate Log(Rank) and Log(Frequency)
    log_ranks = []
    log_freqs = []
    
    for rank, count in enumerate(counts):
        # Rank is 1-based (1, 2, 3...)
        # Log(Rank)
        log_ranks.append(math.log(rank + 1))
        # Log(Frequency)
        log_freqs.append(math.log(count))
        
    return linear_regression(log_ranks, log_freqs)

# --- REAPER Interaction ---

def count_pitches_in_take(take):
    """Returns a dictionary of {pitch: count} for a given MIDI take."""
    histogram = {}
    
    # Iterate all notes
    # reapy notes are iterators
    notes = take.midi_events
    # This might be raw events. Let's use the property 'notes' if available or iterate enumerator
    # reapy Take.notes is simpler
    
    # We'll use RPR for raw speed and reliability on events if reapy abstraction is slow
    # But reapy logic: take.notes
    
    for note in take.notes:
        pitch = note.pitch
        histogram[pitch] = histogram.get(pitch, 0) + 1
            
    return histogram

def analyze_item(item, source_name="Unknown"):
    take = item.active_take
    if not take or not take.map_to_midi_take():
        print(f"Skipping {source_name}: Not a MIDI item.")
        return

    histogram = count_pitches_in_take(take)
    slope, r2, yint = calculate_zipf(histogram)
    
    print(f"Analysis for: {source_name}")
    print(f"  Unique Pitches: {len(histogram)}")
    print(f"  Total Notes:    {sum(histogram.values())}")
    print(f"  Zipf Slope:     {slope:.4f}")
    print(f"  R^2:            {r2:.4f}")
    print("-" * 40)

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # 1. Check for filenames provided in script (Original Use Case)
    # We don't have these files, so we skip unless user provides them.
    midi_files = [
        # "sonifyBiosignals.mid", 
        # "ArvoPart.CantusInMemoriam.mid",
        # ...
    ]
    
    files_found = False
    
    # 2. Check Selected Items (Interactive Use Case)
    # If no files, or meant to be interactive tool
    selected_items = project.selected_items
    
    if len(selected_items) > 0:
        print(f"Analyzing {len(selected_items)} selected item(s)...")
        print("-" * 40)
        for i, item in enumerate(selected_items):
            name = "Selected Item " + str(i+1)
            # Try to get track name
            try:
                name = item.track.name + " (Item)"
            except: 
                pass
            
            analyze_item(item, name)
            
    else:
        print("No selected items found.")
        print("Please select a MIDI item in REAPER to analyze.")

if __name__ == "__main__":
    main()
