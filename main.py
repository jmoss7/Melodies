from play import *
from generate import *
import structures
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button


Builder.load_file('spin.kv')

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


class MyLayout(Widget):
    def update_label(self, input_id, value):
        if input_id == "spinner_key_id":
            self.ids.key_label.text = "Key: " + value
        elif input_id == "spinner_scale_id":
            self.ids.scale_label.text = "Scale: " + value
        elif input_id == "spinner_octave_id":
            self.ids.octave_label.text = "Octave: " + value
        elif input_id == "input_numnotes_id":
            self.ids.numnotes_label.text = "Num Notes: " + value
        else:
            print("you suck")

    def main(self, key, scale, octave, num_notes):
        # Major Chord Melody
        # start = random.randint(12, 92) + 12  # To make it easy to hear
        # start = keys_4[key]
        # instrument = random.randint(0, 127)  # Any random instrument
        # note1 = Note(start, QUARTER_NOTE)  # Base of chord
        # note2 = Note(start + 4, QUARTER_NOTE)
        # note3 = Note(start + 7, QUARTER_NOTE)
        # note4 = note1.duplicate()
        # note4.incrementOctave(1)

        # m = Melody([], instrument=instrument, bpm=100)
        # m.addNote(note1)
        # m.addNote(note2)
        # m.addNote(note3)
        # m.addNote(note4)
        # print(m)

        # m.generateMIDI()
        # m.saveMelodyAs('out.mid')

        instrument = random.randint(0, 127)
        m = Melody([], instrument=instrument, bpm=100)

        scale = scale.lower()
        octave = int(octave)
        num_notes = int(num_notes)
        # generate scale (a list of notes to be used in melody)
        scale1 = generate_scale(key, scale, octave)
        print("Generated %s%d %s scale." % (key, octave, scale))
        print(scale1)

        # randomize notes in scale by choosing {num_notes} random notes
        mel = []
        for i in range(num_notes):
            mel.append(random.choice(scale1))

        # To be an input later on...the number of measures/bars in melody
        bars = 4

        # randomize length of each notes using getRandomStructure function
        lengths = structures.getEqualNoteStructure(bars, num_notes)

        # add the random notes to generate the melody
        for i in range(num_notes):
            curnote = Note(mel[i], lengths[i])#, vel=random.randint(1, 127))
            m.addNote(curnote)

        print("Random melody generated.")
        print(m)

        m.generateMIDI()
        m.saveMelodyAs('out.mid')

        midiToWAV("out.mid", "temp.wav")
        playWAVkivy("temp.wav")

class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()
