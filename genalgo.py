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
        # Create 10 random melodies from the same instrument, create Child w/ melody, add to gen1
        randInstr = chooseRandomInstrument(INSTRUMENT_NP_NS_WITHOUT_CATEGORY)
        for i in range(10):
            m = createMelody(instrument=randInstr, bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
            print(m)
            gen1.getChildren().append(Child(m))


        # Begin rating each of the 5 initial melodies
        # ********* ADD LATER: Option to change instrument ************* 
        print("Generated 10 melodies. Now playing gen 1.")
        # rate each melody
        gen1.giveRatings()
        # sum total rating and normalize for fitness probabilities
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



#       ERROR DETAILS
"""



 more details:
 seems like extraLength gets bigger than originalLength, making value negative

Pasting each incident here:

 ********* SELF ********
Rest4, 4, 0
extraLength = 17 - 14
originalLength: 4
extraLength: 3
self length: 1
*********** REF ************
Rest4, 1, 0
extraLength = 17 - 14
originalLength: 1
extraLength: 3

********* SELF ********
A4, 10, 64
extraLength = 47 - 41
originalLength: 10
extraLength: 6
self length: 4
*********** REF ************
A4, 4, 64
extraLength = 47 - 41
originalLength: 4
extraLength: 6

********* SELF ********
C5, 5, 64
extraLength = 11 - 7
originalLength: 5
extraLength: 4
self length: 1
*********** REF ************
C5, 1, 64
extraLength = 11 - 7
originalLength: 1
extraLength: 4

Seems like it happens when self and ref are the same note
- maybe memory problem???


 extraLength = 10 - 3
originalLength: 10
extraLength: 7
extraLength = 10 - 3
originalLength: 3
extraLength: 7
[INFO   ] [Base        ] Leaving application in progress...
 Traceback (most recent call last):
   File "genalgo.py", line 143, in <module>
     MainApp().run()
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/app.py", line 950, in run
     runTouchApp()
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/base.py", line 582, in runTouchApp
     EventLoop.mainloop()
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/base.py", line 347, in mainloop
     self.idle()
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/base.py", line 391, in idle
     self.dispatch_input()
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/base.py", line 342, in dispatch_input
     post_dispatch_input(*pop(0))
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/base.py", line 248, in post_dispatch_input
     listener.dispatch('on_motion', etype, me)
   File "_event.pyx", line 709, in kivy._event.EventDispatcher.dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/core/window/__init__.py", line 1412, in on_motion
     self.dispatch('on_touch_down', me)
   File "_event.pyx", line 709, in kivy._event.EventDispatcher.dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/core/window/__init__.py", line 1428, in on_touch_down
     if w.dispatch('on_touch_down', touch):
   File "_event.pyx", line 709, in kivy._event.EventDispatcher.dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/uix/widget.py", line 545, in on_touch_down
     if child.dispatch('on_touch_down', touch):
   File "_event.pyx", line 709, in kivy._event.EventDispatcher.dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/uix/widget.py", line 545, in on_touch_down
     if child.dispatch('on_touch_down', touch):
   File "_event.pyx", line 709, in kivy._event.EventDispatcher.dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/uix/behaviors/button.py", line 151, in on_touch_down
     self.dispatch('on_press')
   File "_event.pyx", line 705, in kivy._event.EventDispatcher.dispatch
   File "_event.pyx", line 1248, in kivy._event.EventObservers.dispatch
   File "_event.pyx", line 1132, in kivy._event.EventObservers._dispatch
   File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/kivy/lang/builder.py", line 57, in custom_callback
     exec(__kvlang__.co_value, idmap)
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/spin.kv", line 63, in <module>
     on_press: root.main(spinner_key_id.text, spinner_scale_id.text, spinner_octave_id.text, input_numnotes_id.text, input_bars_id.text)
   File "genalgo.py", line 94, in main
     gen1.advanceToNextGenWith10()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/generation.py", line 215, in advanceToNextGenWith10
     crossMe3 = parents[0].makeCopy()
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/child.py", line 53, in makeCopy
     return Child(self.getData().duplicate())
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/melody.py", line 296, in duplicate
     key_sig=self.keySig)
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/melody.py", line 28, in __init__
     self.length = sum([len(x) for x in contents])
   File "/Users/austinng/calpoly/seniorproj/finalrepo/Melodies/melody.py", line 28, in <listcomp>
     self.length = sum([len(x) for x in contents])
 ValueError: __len__() should return >= 0


"""


#   Got this far
#   Outside of that error, i'm 80% sure that selection/mutation works properly



 




class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()



