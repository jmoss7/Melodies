from note import *
from melody import *
import random


keys_4 = {
	"C": 60,
	"C#": 61,
	"Db": 61,
	"D": 62,
	"D#": 63,
	"Eb": 63,
	"E": 64,
	"Fb": 64,
	"F": 65,
	"F#": 66,
	"Gb": 66,
	"G": 67,
	"G#": 68,
	"Ab": 68,
	"A": 69,
	"A#": 70,
	"Bb": 70,
	"B": 71,
}


def main():
	major = generate_major("C")
	minor = generate_minor("C")

	major.generateMIDI()
	minor.generateMIDI()

	major.saveMelodyAs('major.mid')
	minor.saveMelodyAs('minor.mid')



def generate_major(key):
	# Major Chord Melody
    start = keys_4[key]
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

    return m


def generate_minor(key):
	# Minor Chord Melody
    start = keys_4[key]
    instrument = random.randint(0, 127)  # Any random instrument
    note1 = Note(start, QUARTER_NOTE)  # Base of chord
    note2 = Note(start + 3, QUARTER_NOTE)
    note3 = Note(start + 7, QUARTER_NOTE)
    note4 = note1.duplicate()
    note4.incrementOctave(1)

    m = Melody([], instrument=instrument, bpm=100)
    m.addNote(note1)
    m.addNote(note2)
    m.addNote(note3)
    m.addNote(note4)
    print(m)

    return m



if __name__ == '__main__':
    main()