from melody import *
from note import *
import random

def main():
    # Major Chord Melody
    start = random.randint(12, 92) + 12  # To make it easy to hear
    instrument = random.randint(0, 127)  # Any random instrument
    note1 = Note(start, QUARTER_NOTE)  # Base of chord
    note2 = Note(start + 4, QUARTER_NOTE)
    note3 = Note(start + 7, QUARTER_NOTE)
    note4 = note1.duplicate()
    note4.incrementOctave(1)

    m = Melody([], instrument=instrument, bpm=100)
    m.addNote(note1)
    m.addNote(note2)
    m.addNote(note3)
    m.addNote(note4)
    print(m)

    m.generateMIDI()
    m.saveMelodyAs('out.mid')

if __name__ == '__main__':
    main()