from play import *
from melodygen import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
import shutil

MELODY_SAVE_NUMBER: int = 1
MELODY_FILENAME: str = "out.mid"

Builder.load_file('spin.kv')

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
        elif input_id == "input_bars_id":
            self.ids.bars_label.text = "Num Bars: " + value
        elif input_id == "spinner_instrument_id":
            self.ids.instrument_label.text = "Instrument: " + value
        else:
            print("you suck")

    def save_melody(self):
        global MELODY_SAVE_NUMBER
        global MELODY_FILENAME
        shutil.copyfile(MELODY_FILENAME, "saved_melody_" + str(MELODY_SAVE_NUMBER) + ".mid")
        MELODY_SAVE_NUMBER += 1

    def main(self, key, scale, octave, num_notes, num_bars, instrument):
        selected_instrument = instrument
        scale = scale.lower()
        key = key.lower()
        key = key.capitalize()

        if scale == 'choose scale' or scale == 'Random':
            scale = ""

        try:
            octave = int(octave)
        except:
            octave = -2

        if key == 'Choose key' or key == 'Random':
            key = ""

        try:
            bars = int(num_bars)
        except:
            bars = -1
        if instrument == 'Choose Instrument' or instrument == 'Random':
            m = createMelody(-3, bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
        else:
            m = createMelody(getMIDINumber(selected_instrument), bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
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
