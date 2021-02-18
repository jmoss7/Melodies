from melody import *
from note import *
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
    def spinner_clicked(self, value):
        self.ids.click_label.text = f'{value}'

    def main(self, key):
        # Major Chord Melody
        # start = random.randint(12, 92) + 12  # To make it easy to hear
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

        m.generateMIDI()
        m.saveMelodyAs('out.mid')


class MainApp(App):
    def build(self):
        return MyLayout()





if __name__ == '__main__':
    MainApp().run()
