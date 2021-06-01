import shutil
from play import *
from melodygen import *
from melodystack import MelodyStack
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from generation import Generation
from child import Child
from numpy.random import choice
import global_vars

prevH = 0
prevW = 0
MELODY_SAVE_NUMBER: int = 1
MELODY_FILENAME_MIDI: str = "../temp/out.mid"
MELODY_FILENAME_WAV: str = "../temp/temp.wav"

Builder.load_file('spin.kv')

class MyLayout(Widget):
    def update_label(self, input_id, value):
        if input_id == "spinner_key_id":
            self.ids.key_label.text = "Key: " + value
        elif input_id == "spinner_scale_id":
            self.ids.scale_label.text = "Scale: " + value
        elif input_id == "spinner_octave_id":
            self.ids.octave_label.text = "Octave: " + value
        elif input_id == "input_bars_id":
            self.ids.bars_label.text = "Num Bars: " + value
        elif input_id == "spinner_instrument_id":
            self.ids.instrument_label.text = "Instrument: " + value
        elif input_id == "generation_label":
            self.ids.generation_label.text = "Generation: " + value
        elif input_id == "current_label":
            self.ids.current_label.text = "Melody: " + value

    def save_melody(self):
        global MELODY_SAVE_NUMBER
        global MELODY_FILENAME_MIDI
        global MELODY_FILENAME_WAV
        shutil.copyfile(MELODY_FILENAME_MIDI, "../saved/saved_melody_" + str(MELODY_SAVE_NUMBER) + ".mid")
        shutil.copyfile(MELODY_FILENAME_WAV, "../saved/saved_melody_" + str(MELODY_SAVE_NUMBER) + ".wav")
        MELODY_SAVE_NUMBER += 1

    # rates current melody increments global index
    def giveRating(self, curRating):

        curChild = global_vars.gen1.getChildren()[global_vars.rating_index]

        curRating = float(int(curRating))
        curChild.setRating(curRating)

        global_vars.rating_index += 1

        if global_vars.rating_index <= 9:
            curChild = global_vars.gen1.getChildren()[global_vars.rating_index]
            m = curChild.getData()
            m.generateMIDI()
            m.saveMelodyAs('../temp/out.mid')
            midiToWAV("../temp/out.mid", "../temp/temp.wav")
            global_vars.melody_number += 1
            self.update_label("current_label", str(global_vars.melody_number))
            playWAVkivy("../temp/temp.wav")
        else:
            global_vars.gen1.calculateTotalRating()
            global_vars.gen1.normalizeFitness()
            global_vars.gen1.findHighest()
            print(global_vars.gen1.getTopRatingIdx())
            global_vars.gen1.advanceToNextGenWith10()
            global_vars.rating_index = 0
            global_vars.generation_number += 1
            self.update_label("generation_label", str(global_vars.generation_number))
            global_vars.melody_number = 1
            self.update_label("current_label", str(global_vars.melody_number))
            curChild = global_vars.gen1.getChildren()[global_vars.rating_index]
            m = curChild.getData()
            m.generateMIDI()
            m.saveMelodyAs('../temp/out.mid')
            midiToWAV("../temp/out.mid", "../temp/temp.wav")
            playWAVkivy("../temp/temp.wav")







    def main(self, key, scale, octave, num_bars, instrument):
        global rating_index, gen1
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
            chosenInstrument = -3
        else:
            chosenInstrument = getMIDINumber(instrument)

        # **************** MAKE SURE TO CHECK BAD INPUT **************
        # Begin genetic algorithm
        # create the first generation of melodies
        global_vars.gen1 = Generation([], 1)
        print("Creating first generation...........")
        global_vars.gen1.createFirstGenWith10(scale, octave, key, bars, chosenInstrument)
        # Begin rating each of the 10 initial melodies
        # rate each melody
        # sum total rating and normalize for fitness probabilities
        # ********* ADD LATER: Option to change instrument *************


        m = global_vars.gen1.getChildren()[global_vars.rating_index].getData()
        m.generateMIDI()
        m.saveMelodyAs('../saved/out.mid')
        midiToWAV("../saved/out.mid", "../temp/temp.wav")
        playWAVkivy("../temp/temp.wav")
        global_vars.generation_number = 1
        self.update_label("generation_label", str(global_vars.generation_number))
        global_vars.melody_number = 1
        self.update_label("current_label", str(global_vars.melody_number))
"""
        print("Generated 10 melodies. Now playing gen 1.")
        gen1.giveRatings()
        gen1.calculateTotalRating()
        gen1.normalizeFitness()

        # Use ratings to advance to next generation, or stop.
        option = input("[a]dvance to next gen? or [s]top: ")
        while option == "a" or option == "A":
            gen1.advanceToNextGenWith10()
            print("Now playing gen %d." % gen1.getGen())
            gen1.giveRatings()
            gen1.calculateTotalRating()
            gen1.normalizeFitness()
            option = input("[a]dvance to next gen? or [s]top: ")
        print("Finished after %d generations." % gen1.getGen())
"""




# notes
# 1) Working on option to restart with 10 new random melodies
# 2) Not using num_notes, can probably remove the option from kivy
# 3) Might add option to change instrument/octave/scale during genalgo



 




class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()



