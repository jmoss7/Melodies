from note import *
from melody import *
import random


# midi mappings from C4 to B4
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

# midi mappings from C0 to B0
keys_0 = {
	"C": 12,
	"C#": 13,
	"Db": 13,
	"D": 14,
	"D#": 15,
	"Eb": 15,
	"E": 16,
	"Fb": 16,
	"F": 17,
	"F#": 18,
	"Gb": 18,
	"G": 19,
	"G#": 20,
	"Ab": 20,
	"A": 21,
	"A#": 22,
	"Bb": 22,
	"B": 23,
}

# 
scales = {
	"major": [0, 2, 4, 5, 7, 9, 11, 12],
	"minor": [0, 2, 3, 5, 7, 8, 10, 12],
	"hminor": [0, 2, 3, 5, 7, 8, 11, 12]
}

# Input: Key, scale, octave, number of notes in melody
# Output: Melody in 4/4 at 100bpm, all quarter notes
def main():
	# Generate random instrument for melody
	instrument = random.randint(0, 127)
	m = Melody([], instrument=instrument, bpm=100)

	# generate scale (a list of notes to be used in melody)
	key = input("Choose key (e.g. D#): ")
	scale = input("Choose scale (major, minor, or hminor): ")
	octave = int(input("Choose octave number (from 0 to 7): "))
	scale1 = getScale(key, scale, octave)
	print("Generated %s%d %s scale." % (key, octave, scale))
	print(scale1)

	# randomize notes in scale by choosing {num_notes} random notes
	num_notes = int(input("How many notes in your melody? "))
	mel = []
	for i in range(num_notes):
		mel.append(random.choice(scale1))


	# add the random notes to generate the melody
	for note in mel:
		curnote = Note(note, QUARTER_NOTE)
		m.addNote(curnote)

	print("Random melody generated.")
	print(m)

	m.generateMIDI()
	m.saveMelodyAs('out.mid')


# generates scale from from the given key,scale, & octave
def getScale(key, scale, octave):
	out = []
	for i in range(len(scales[scale])):
		out.append(keys_0[key] + (12 * octave) + scales[scale][i])
	return out





# generate major chord melody
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


# generate minor chord melody
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