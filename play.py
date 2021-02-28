from midi2audio import FluidSynth
from playsound import playsound

def midiToWAV(in_fname):
    fs = FluidSynth()
    fs.midi_to_audio(in_fname, "temp.wav")

def playWAV(fname):
    playsound(fname)