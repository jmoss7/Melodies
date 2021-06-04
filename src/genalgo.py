import shutil
from play import *
from melodygen import *
from melodystack import MelodyStack
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.lang import Builder
from generation import Generation
import global_vars

MELODY_SAVE_NUMBER: int = 1
MELODY_FILENAME_MIDI: str = "../temp/out.mid"
MELODY_FILENAME_WAV: str = "../temp/temp.wav"
global_vars.MELODY_STACK = MelodyStack()
TEMP_FOLD = "../temp/"

Builder.load_file('spin.kv')

class MyLayout(TabbedPanel):
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
            self.ids.generation_label.text = value

    def addMelToStack(self):
        m = global_vars.gen1.getChildren()[global_vars.rating_index].getData()
        if type(m) == Melody:
            idx = global_vars.MELODY_STACK.findFirstEmpty()
            global_vars.MELODY_STACK.addMelody(idx, m)
            if idx != -1:
                self.ids['fullStackBut'].background_color = 0.0, 1.0, 0.0, 1.0
            buttonId = "but" + str(idx+1)
            self.ids[buttonId].background_color = 0.0, 1.0, 0.0, 1.0
            midName = TEMP_FOLD + "stack_spot" + str(idx+1) + ".mid"
            wavName = TEMP_FOLD + "stack_spot" + str(idx+1) + ".wav"
            m.file.save(midName)
            midStackName = TEMP_FOLD + "melodyStack.mid"
            wavStackName = TEMP_FOLD + "melodyStack.wav"
            global_vars.MELODY_STACK.saveMelodyStackAs(midStackName)
            midiToWAV(midName, wavName)
            midiToWAV(midStackName, wavStackName)
        else:
            print("did not have a melody to add to stack")

    def clearStack(self):
        midTrackName = ""
        for i in range(10):
            midTrackName = TEMP_FOLD + "stack_spot" + str(i+1) + ".mid"
            wavTrackName = TEMP_FOLD + "stack_spot" + str(i+1) + ".wav"
            buttonId = "but" + str(i+1)
            self.ids[buttonId].background_color = 1.0, 0.0, 0.0, 1.0
            self.ids['fullStackBut'].background_color = 1.0, 0.0, 0.0, 1.0
            if global_vars.MELODY_STACK.melsStatus[i] == True:
                global_vars.MELODY_STACK.deleteMelody(i)
                global_vars.MELODY_STACK.subMelodies[i].file.save(midTrackName)
                midiToWAV(midTrackName, wavTrackName)
                global_vars.MELODY_STACK.deleteMelody(i)
        midStackName = TEMP_FOLD + "melodyStack.mid"
        wavStackName = TEMP_FOLD + "melodyStack.wav"
        global_vars.MELODY_STACK.saveMelodyStackAs(midStackName)
        midiToWAV(midStackName, wavStackName)

    def playIndMel(self, trackNum):
        if global_vars.MELODY_STACK.melsStatus[trackNum-1]:
            wavName = TEMP_FOLD + "stack_spot" + str(trackNum) + ".wav"
            playWAVkivy(wavName)
        else:
            print("Nothing there to play")

    def delIndMel(self, trackNum):
        buttonId = "but" + str(trackNum)
        self.ids[buttonId].background_color = 1.0, 0.0, 0.0, 1.0
        global_vars.MELODY_STACK.deleteMelody(trackNum-1)
        midName = TEMP_FOLD + "stack_spot" + str(trackNum) + ".mid"
        wavName = TEMP_FOLD + "stack_spot" + str(trackNum) + ".wav"
        midStackName = TEMP_FOLD + "melodyStack.mid"
        wavStackName = TEMP_FOLD + "melodyStack.wav"
        global_vars.MELODY_STACK.saveMelodyStackAs(midStackName)
        global_vars.MELODY_STACK.subMelodies[trackNum-1].file.save(midName)
        midiToWAV(midName, wavName)
        midiToWAV(midStackName, wavStackName)
        stackCheck = global_vars.MELODY_STACK.numberOfFilledTracks()
        if stackCheck == 0:
            self.ids['fullStackBut'].background_color = 1.0, 0.0, 0.0, 1.0

    def playMelStack(self):
        playWAVkivy(TEMP_FOLD + "melodyStack.wav")
        print(global_vars.MELODY_STACK)

    def save_melody(self):
        global MELODY_SAVE_NUMBER
        global MELODY_FILENAME_MIDI
        global MELODY_FILENAME_WAV
        try:
            shutil.copyfile(MELODY_FILENAME_MIDI + "a", "../saved/saved_melody_" + str(MELODY_SAVE_NUMBER) + ".mid")
            shutil.copyfile(MELODY_FILENAME_WAV, "../saved/saved_melody_" + str(MELODY_SAVE_NUMBER) + ".wav")
            MELODY_SAVE_NUMBER += 1
        except:
            "Unable to save melody"

    # replays the current melody
    def replay_melody(self):
        if str(global_vars.soundPlayer.state) != "play":
            print("Replaying the current melody")
            playWAVkivy("../temp/temp.wav")

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
            self.update_label("generation_label", "Generation: {}, Melody: {}".format(
                              str(global_vars.generation_number), str(global_vars.melody_number)))
            playWAVkivy("../temp/temp.wav")
        else:
            global_vars.gen1.calculateTotalRating()
            global_vars.gen1.normalizeFitness()
            global_vars.gen1.findHighest()
            print(global_vars.gen1.getTopRatingIdx())
            global_vars.gen1.advanceToNextGenWith10()
            global_vars.rating_index = 0
            global_vars.generation_number += 1
            global_vars.melody_number = 1
            self.update_label("generation_label", "Generation: {}, Melody: {}".format(
                              str(global_vars.generation_number), str(global_vars.melody_number)))
            curChild = global_vars.gen1.getChildren()[global_vars.rating_index]
            m = curChild.getData()
            m.generateMIDI()
            m.saveMelodyAs('../temp/out.mid')
            midiToWAV("../temp/out.mid", "../temp/temp.wav")
            playWAVkivy("../temp/temp.wav")

    def main(self, key, scale, octave, num_bars, instrument):
        global rating_index, gen1

        scale = scale.lower()
        key = key.lower()
        key = key.capitalize()

        if scale == 'choose scale' or scale == 'random':
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
        genScale, genOctave, genKey, genBars, genInstrument = global_vars.gen1.createFirstGenWith10(scale, octave, key, bars, chosenInstrument)
        self.update_label("spinner_key_id", genKey)
        self.update_label("spinner_scale_id", genScale.capitalize())
        self.update_label("spinner_octave_id", str(genOctave))
        self.update_label("input_bars_id", str(genBars))
        self.update_label("spinner_instrument_id", getInstrument(genInstrument))

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
        global_vars.melody_number = 1
        self.update_label("generation_label", "Generation: {}, Melody: {}".format(
                           str(global_vars.generation_number), str(global_vars.melody_number)))
        if global_vars.MELODY_STACK.numberOfFilledTracks() == 0:
            self.clearStack()

# notes
# 1) Working on option to restart with 10 new random melodies
# 2) Might add option to change instrument/octave/scale during genalgo

class MainApp(App):
    def build(self):
        if global_vars.MELODY_STACK.numberOfFilledTracks() == 0:
            MyLayout().clearStack()
        return MyLayout()

if __name__ == '__main__':
    MainApp().run()



