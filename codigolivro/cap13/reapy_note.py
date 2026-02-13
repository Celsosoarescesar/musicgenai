"""
reapy_note.py

Demonstrates how to create a class to encapsulate a musical note.
This allows for Object-Oriented Music Generation.

Ported from note.py
"""

import reapy

# Constants
C4 = 60
QN = 1.0 # Quarter Note usually 1.0 beats (or 0.5 sec depending on logic) 
# In reapy QN usually refers to beats.

class Note:

    def __init__(self, pitch=C4, duration=QN, dynamic=100, panning=64):
        """Initializes a Note object."""
        self.pitch = pitch          # MIDI Pitch (0-127)
        self.duration = duration    # Duration (Beats)
        self.dynamic = dynamic      # Velocity (0-127)
        self.panning = panning      # Pan (0-127, Center=64)

    # --- Getters and Setters ---
    
    def get_pitch(self):
        return self.pitch

    def set_pitch(self, pitch):
        if 0 <= pitch <= 127:
            self.pitch = pitch
        else:
            print(f"TypeError: Note.set_pitch(): pitch 0-127 (got {pitch})")

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        # In Python we assume float/int is fine
        self.duration = float(duration)

    def get_dynamic(self):
        return self.dynamic
        
    def set_dynamic(self, dynamic):
        self.dynamic = max(0, min(127, int(dynamic)))
        
    def get_panning(self):
        return self.panning

    def set_panning(self, pan):
        self.panning = max(0, min(127, int(pan)))

    # --- REAPER Integration ---

    def insert_midi(self, take, start_qn):
        """
        Inserts this note into a REAPER take at start_qn.
        Also inserts a Pan CC message if panning is not None.
        """
        end_qn = start_qn + self.duration
        
        # Insert Note
        reapy.RPR.MIDI_InsertNote(
            take.id, 
            False,      # Selected
            False,      # Muted
            start_qn, 
            end_qn, 
            0,          # Channel
            int(self.pitch), 
            int(self.dynamic), 
            True        # NoSort
        )
        
        # Insert Pan (CC 10)
        reapy.RPR.MIDI_InsertCC(
            take.id,
            False,      # Selected
            False,      # Muted
            start_qn,
            176,        # Status (CC Ch 1)
            10,         # CC Number (Pan)
            int(self.panning),
            True        # NoSort
        )

def main():
    try:
        project = reapy.Project()
        print("Connected to REAPER.")
    except Exception:
        print("Error: Could not connect to REAPER.")
        return

    # Create Track
    track = project.add_track()
    track.name = "OOP Note Demo"
    track.select()
    
    # Create MIDI Item
    total_duration = 10.0 # arbitrary
    bpm = 120
    qn_to_sec = 60 / bpm
    total_sec = total_duration * qn_to_sec
    
    item = track.add_item(0, total_sec)
    take = item.active_take
    if not take: return
    
    # Create Note Objects
    print("Creating Note objects...")
    n1 = Note(C4, QN, 100, 64)      # Middle C, Center
    n2 = Note(C4 + 4, QN, 80, 0)    # E4, Left
    n3 = Note(C4 + 7, QN * 2, 120, 127) # G4, Right, Long
    
    notes_list = [n1, n2, n3]
    
    # Sequence them
    current_qn = 0.0
    for note in notes_list:
        print(f"Inserting Note: Pitch={note.get_pitch()}, Dur={note.get_duration()}, Pan={note.get_panning()}")
        note.insert_midi(take, current_qn)
        current_qn += note.get_duration()
        
    reapy.RPR.MIDI_Sort(take.id)
    reapy.RPR.CSurf_OnPlay()
    print("Done! Notes inserted via OOP.")

if __name__ == "__main__":
    main()
