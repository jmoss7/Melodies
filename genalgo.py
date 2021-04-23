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

        # create the first generation with empty list of children
        gen1 = Generation([], 1)
        print("Creating first generation...........")
        # Create 5 random melodies from the same instrument, create Child w/ melody, add to gen1
        randInstr = chooseRandomInstrument(INSTRUMENT_NP_NS_WITHOUT_CATEGORY)
        for i in range(5):
            m = createMelody(instrument=randInstr, bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
            print(m)
            gen1.getChildren().append(Child(m))


        # Begin rating each of the 5 initial melodies
        # ********* ADD LATER: Option to change instrument ************* 
        print("Generated 5 melodies. Now playing gen 1.")
        # rate each melody
        gen1.giveRatings()
        # sum total rating and normalize for fitness probabilities
        gen1.calculateTotalRating()
        gen1.normalizeFitness()



        # Use ratings to advance to next generation, or stop.
        option = input("[a]dvance to next gen? or [s]top: ")
        while option == "a" or option == "A":
            gen1.advanceToNextGen()
            print("Now playing gen %d." % gen1.getGen())
            gen1.giveRatings()
            gen1.calculateTotalRating()
            gen1.normalizeFitness()
            option = input("[a]dvance to next gen? or [s]top: ")
        print("Finished after %d generations." % gen1.getGen())



#       This error appears sometimes:
"""
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/spin.kv", line 63, in <module>
     on_press: root.main(spinner_key_id.text, spinner_scale_id.text, spinner_octave_id.text, input_numnotes_id.text, input_bars_id.text)
   File "genalgo.py", line 94, in main
     gen1.giveRatings()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/generation.py", line 100, in giveRatings
     m.generateMIDI()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/melody.py", line 267, in generateMIDI
     noteLen = self.sequence[i].getLengthTime(TICKS_PER_BEAT)
 IndexError: list index out of range



This one too
   File "genalgo.py", line 94, in main
     gen1.advanceToNextGen()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/generation.py", line 168, in advanceToNextGen
     parents = self.selection()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/generation.py", line 127, in selection
     replace=False, p=self.getProbabilities())
   File "mtrand.pyx", line 926, in numpy.random.mtrand.RandomState.choice
 ValueError: 'a' and 'p' must have same size

"""




#   Got this far
#   Outside of that error, i'm 80% sure that selection/mutation works properly
#   Can't see how well it'll work yet since it doesn't get far before that error happens



 




class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()



