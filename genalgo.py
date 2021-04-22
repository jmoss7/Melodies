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
        print("Generated 5 melodies.")
        ######gen1.giveRatings()
        # sum total rating and normalize for fitness probabilities
        ######gen1.calculateTotalRating()
        #######gen1.normalizeFitness()





        # ************ TESTING MUTATE FUNCTION HERE **************


        print("Playing first melody...")
        firstChild = gen1.getChildren()[0]
        mel = firstChild.getData()
        mel.generateMIDI()
        mel.saveMelodyAs('out.mid')
        midiToWAV("out.mid", "temp.wav")
        playWAVkivy("temp.wav")

        print(firstChild.getData())

        testMutate = False
        userInput = input("Mutate (y/n) ? ")
        if userInput == "y":
            testMutate = True
        else:
            testMutate = False

        while testMutate == True:
            firstChild.mutate()
            newmel = firstChild.getData()
            print("Playing mutated melody...")
            newmel.generateMIDI()
            newmel.saveMelodyAs('out.mid')
            midiToWAV("out.mid", "temp.wav")
            playWAVkivy("temp.wav")

            print(firstChild.getData())

            userInput = input("Mutate (y/n) ? ")
            if userInput == "y":
                testMutate = True
            else:
                testMutate = False

        print("Done mutating. Goodbye!")

        # ***** END TEST MUTATE WHY IS THE MELODY NOT CHANGING **********






        # select two parents to be crossed, and one (non-parent) survivor
        ########parent1 = gen1.selection()
        #print("Parent 1 Fitness: %f" % parent1.getFitness())
        #print("Rating %f" % parent1.getRating())
        ########parent2 = gen1.selection()
        #print("Parent 2 Fitness: %f" % parent2.getFitness())
        #print("Rating: %f" % parent2.getRating())
        ########othersurvivor = gen1.selection()
        #print("Survivor Fitness: %f" % othersurvivor.getFitness())
        #print("Rating: %f" % othersurvivor.getRating())




        # TO DO: CREATE NEXT GENERATION - In generation.py?????



        




        #m.generateMIDI()
        #m.saveMelodyAs('out.mid')

        #midiToWAV("out.mid", "temp.wav")
        #playWAVkivy("temp.wav")

class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()



