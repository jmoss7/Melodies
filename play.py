from midi2audio import FluidSynth
from kivy.core.audio import SoundLoader

def playMIDI(fname):
    fs = FluidSynth()
    fs.play_midi(fname)

def midiToWAV(in_fname, out_fname):
    fs = FluidSynth()
    fs.midi_to_audio(in_fname, out_fname)

def playWAVkivy(filename):
    sound = SoundLoader.load(filename)
    if sound:
        sound.play()
