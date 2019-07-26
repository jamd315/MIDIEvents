import mido

from ChordEvents.__version__ import __version__
from ChordEvents.Note import Note
from ChordEvents.Chord import Chord
from ChordEvents.ChordEventLoop import ChordEventLoop
from ChordEvents.LoopbackInput import LoopbackInput

mido.set_backend("mido.backends.rtmidi")  # TODO config this

__all__ = [
    "Note",
    "Chord",
    "ChordEventLoop",
    "LoopbackInput"
]