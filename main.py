from play import *
from melodygen import *
from melodystack import MelodyStack
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button

"""def melodyStackBeta():
    ms = MelodyStack()

    options = "\nMelodies (Melody Stack Beta on Terminal Version)\n"
    options += "------------------------\n"
    options += "1. Play\n2. Add Melody\n3. Remove Melody\n4. Swap Melodies\n"
    options += "5. Print Melody Stack\n6. Set Key Signature\n7. Set Scale\n"
    options += "8. Loop Track\n9. Exit\n"

    print(options)
    nbr = input("Choose a number: ").strip()

    while nbr != '9':
        if nbr == '1':
            single = input("Play all tracks together (y/n)? ").strip()
            if single.lower() == 'y':
                ms.saveMelodyStackAs("out2.mid")
                midiToWAV("out2.mid", "temp2.wav")
                playWAVkivy("temp2.wav")
                ms.file.print_tracks()
            else:
                trackNo = int(input("Which track number? ").strip())
                m = ms.getSpecificMelody(trackNo).duplicate()
                m.generateMIDI()
                in_fn = "out2track{}.mid".format(trackNo)
                out_fn = "temp2track{}.wav".format(trackNo)
                m.saveMelodyAs(in_fn)
                midiToWAV(in_fn, out_fn)
                playWAVkivy(out_fn)
        elif nbr == '2':
            print("\n1. Copy Existing\n2. New Melody\n3. Back to Main Menu\n")
            nbr2 = input("Choose a number: ").strip()
            if nbr2 == '1':
                trackNo = int(input("Which track to copy from? ").strip())
                destNo = int(input("Which track to copy to? ").strip())
                ms.duplicateTrack(trackNo, destNo)
            elif nbr2 == '2':
                octv = int(input("Which octave: ").strip())
                scale1 = generate_scale(ms.getKeySignature(), ms.getScale(),
                                        octv)
                numNotes = int(input("How many notes? ").strip())
                meas = int(input("How many measures? ").strip())
                mel = []
                for i in range(numNotes):
                    mel.append(random.choice(scale1))

                # randomize length of each notes using getRandomStructure func
                lengths = structures.getEqualNoteStructure(meas, numNotes)

                m = Melody([], instrument=0, bpm=ms.getBPM())

                # add the random notes to generate the melody
                for i in range(numNotes):
                    curnote = Note(mel[i], lengths[i])
                    m.addNote(curnote)

                tNo = int(input("Which track number? ").strip())
                ms.addMelody(tNo, m)
        elif nbr == '3':
            tNo = int(input("Which track number? ").strip())
            ms.deleteMelody(tNo)
        elif nbr == '4':
            src = int(input("Swap track... ").strip())
            dest = int(input("With track... ").strip())
            ms.moveMelodies(src, dest)
        elif nbr == '5':
            print(ms)
        elif nbr == '6':
            key = input("Which key? ").strip()
            ms.setKeySignature(key)
        elif nbr == '7':
            scale = input("Which scale? ").strip()
            ms.setScale(scale)
        elif nbr == '8':
            tNo = int(input("Which track number? ").strip())
            nL = int(input("How many times do you want to loop? ").strip())
            ms.loopTrack(tNo, nL)

        print(options)
        nbr = input("Choose a number: ").strip()"""

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

        m = createMelody(bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
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



