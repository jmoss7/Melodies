from play import *
from melodygen import *
from melodystack import MelodyStack
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button

from generation import Generation
from child import Child



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
        else:
            print("you suck")

    def save_melody(self):
        return

    def main(self, key, scale, octave, num_notes, num_bars):
        scale = scale.lower()
        key = key.lower()
        key = key.capitalize()

        if scale == 'choose scale':
            scale = ""

        try:
            octave = int(octave)
        except:
            octave = -2

        if key == 'choose key':
            key = ""

        try:
            num_notes = int(num_notes)
        except:
            num_notes = -2

        try:
            bars = int(num_bars)
        except:
            bars = -1




        # **************** NEEDS ERROR CHECKING, EDGE CASES, ETC **************
        # Begin genetic algorithm.

        # gen1 is the first generation of Children objects
        gen1 = Generation([], 1)
        print("Creating first generation...........")
        # Create 5 random melodies from the same instrument, create Child w/ melody, append to gen1
        randInstr = chooseRandomInstrument(INSTRUMENT_NP_NS_WITHOUT_CATEGORY)
        for i in range(5):
            m = createMelody(instrument=randInstr, bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
            print(m)
            gen1.getChildren().append(Child(m))


        # Begin rating each of the 5 melodies
        # ********* ADD LATER: Option to change instrument ************* 
        print("Generated 5 melodies. Rate each one from 1 to 5:")
        count = 0
        for child in gen1.getChildren():
            count += 1
            m = child.getData()
            m.generateMIDI()
            m.saveMelodyAs('out.mid')
            print("Playing Melody %d..." % count)
            midiToWAV("out.mid", "temp.wav")
            playWAVkivy("temp.wav")
            curOption = input("Rate this melody 1-10 or type 'replay' to replay: ")
            while (curOption == "replay" or curOption == "Replay"):
                print("Replaying melody...")
                playWAVkivy("temp.wav")
                curOption = input("Rate this melody 1-10 or type 'replay' to replay: ")
            # **************** NEED ERROR CHECKING HERE ******************
            # if option is not int from 1-10, error
            # else:
            # set rating of current melody
            curRating = int(curOption)
            child.setFitness(float(curRating))


        print("************** PRINTING FITNESS *********************")

        count = 0
        for child in gen1.getChildren():
            count += 1
            print("Rating: %d: %d" % (count, child.getFitness()))

        gen1.calculateTotalFitness();
        print("Total Fitness: %d" % gen1.getTotalFitness())
        gen1.normalizeFitness();


        print("NORMALIZED")
        count = 0
        for child in gen1.getChildren():
            count += 1
            print("Fitness %d: %d" % (count, child.getFitness()))



        #for child in gen1:




        #m.generateMIDI()
        #m.saveMelodyAs('out.mid')

        #midiToWAV("out.mid", "temp.wav")
        #playWAVkivy("temp.wav")

class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()



