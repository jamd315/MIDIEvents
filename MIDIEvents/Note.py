import logging
import re

logger = logging.getLogger("MIDIEvents")


class Note:
    pitch_class_map = {  # Overflow is where octave changes
        0: 'C',
        1: 'C#',
        2: 'D',
        3: 'D#',
        4: 'E',
        5: 'F',
        6: 'F#',
        7: 'G',
        8: 'G#',
        9: 'A',
        10: 'A#',
        11: 'B'
    }
    pitch_class_map_complement = {j: i for i, j in pitch_class_map.items()}

    def __init__(self, *args, note_str=None, note=None, octave=None, midi=None):
        # Constructor pre-processing sets the same variables as passed to __init__ to let logic below finalize construction

        # Implicit argument mapping
        if len(args) == 1 and isinstance(args[0], str):
            note_str = args[0]
        elif len(args) == 1 and isinstance(args[0], int):
            midi = args[0]
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
            note = args[0]
            octave = args[1]
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], str):  # Probably won't actually happen, Note(4, "A")
            octave = args[0]
            note = args[1]
        
        if note_str and any(x is not None for x in [note, octave, midi]):
            raise TypeError("Passing both keyword arguments for note/octave/midi is not supported while using positional argument note_str")
        
        if note_str:
            match = re.match("([a-zA-Z#b]+)([0-9-]+)", note_str)
            if not match:
                raise ValueError("Invalid entry for note_str")
            note = match.group(1)
            octave = int(match.group(2))
            logger.debug("Note created using __init__ note_str")

        if note:
            note = note.upper()

        if note is not None and octave is not None:  # From note and octave
            if len(note) == 2 and note[-1] == "B":  # Flat, convert to sharp
                pc = self.pitch_class_map_complement[note[0]] - 1  # Decrement pitch class
                if pc == -1:  # Underflow
                    note = "B"
                    octave -= 1
                else:
                    note = self.pitch_class_map[pc]
            self.note = note
            self.octave = octave
            self.midi = self._note_octave_to_midi(note, octave)
            logger.debug("Note created using __init__ note and octave")
        elif midi is not None:  # From MIDI
            self.note, self.octave = self._midi_to_note_octave(midi)
            self.midi = midi
            logger.debug("Note created using __init__ MIDI")
        else:
            raise TypeError
        self.pc = self.pitch_class_map_complement[self.note]
        self.freq = round(2 ** ((self.midi - 69) / 12) * 440, 2)
        if self.midi not in range(128):
            logger.warning("Note created outside normal MIDI range of 0 to 127 (inclusive)")

    def __str__(self):
        return self.note + str(self.octave)
    
    def __repr__(self):
        return "Note(" + str(self) + ")"

    def __gt__(self, other):
        return self.midi > other.midi
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.midi == other.midi

    def __hash__(self):
        return hash(self.midi)

    @classmethod
    def _note_octave_to_midi(cls, note, octave):
        assert isinstance(note, str)
        assert isinstance(octave, int)
        pc = cls.pitch_class_map_complement[note]
        midi = octave * 12 + pc + 12
        return midi

    @classmethod
    def _midi_to_note_octave(cls, m):
        assert isinstance(m, int)
        m -= 12  # C0 is midi 12
        octave, note = divmod(m, 12)
        note = cls.pitch_class_map[note]
        return note, octave
