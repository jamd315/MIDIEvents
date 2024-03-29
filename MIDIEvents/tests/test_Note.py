import logging
import unittest

from MIDIEvents import Note

logger = logging.getLogger("MIDIEvents")


class TestNote(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Note("A4").midi, 69)
        self.assertEqual(Note("Cb4").midi, 59)  # Underflow and decrement the octave
        self.assertEqual(Note("F#2").midi, 42)
        self.assertEqual(Note("F#9").midi, 126)

        self.assertEqual(Note("A", 4).midi, 69)
        self.assertEqual(Note("Cb", 4).midi, 59)
        self.assertEqual(Note("F#", 2).midi, 42)

        self.assertEqual(Note(69).pc, 9)
        self.assertEqual(Note(69).octave, 4)

        self.assertEqual(Note(69), Note(4, "A"))

        with self.assertRaises(TypeError):
            Note([])

        with self.assertRaises(TypeError):
            Note(note_str="A4", midi=69)

        with self.assertRaises(ValueError):
            Note(note_str="4A")
    
    def test_from_lowercase(self):
        self.assertEqual(Note("a4").midi, 69)
        self.assertEqual(Note("ab5").midi, 80)
        self.assertEqual(Note("c#3").midi, 49)

    def test_string(self):
        n1 = Note("A4")
        self.assertEqual(str(n1), "A4")
    
    def test_repr(self):
        n1 = Note("A4")
        self.assertEqual(repr(n1), "Note(A4)")
    
    def test_greater_than(self):
        n1 = Note(69)
        n2 = Note(70)
        self.assertGreater(n2, n1)
        self.assertGreater(n2.midi, n1.midi)
    
    def test_equality(self):
        n1 = Note("A4")
        n2 = Note(69)
        self.assertEqual(n1, n2)
        self.assertNotEqual(n1, True)
    
    def test_freq(self):
        self.assertEqual(Note("A4").freq, 440.00)
        self.assertEqual(Note("C6").freq, 1046.50)
        self.assertEqual(Note("C0").freq, 16.35)
        self.assertEqual(Note("A-1").freq, 13.75)
        self.assertEqual(Note("Cb4").freq, 246.94)
        self.assertEqual(Note("B3").freq, 246.94)
    
    def test_MIDI_range_warn(self):
        with self.assertLogs(logger=logger, level="WARNING"):
            Note("A11")
