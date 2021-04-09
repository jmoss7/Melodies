from midi2audio import FluidSynth
from playsound import playsound
from kivy.core.audio import SoundLoader

def playMIDI(fname: str):
    """ Play the MIDI file called fname through FluidSynth """

    fs = FluidSynth()
    fs.play_midi(fname)

def midiToWAV(in_fname: str, out_fname: str):
    """ Convert the MIDI file called in_fname to the WAV file
        called out_fname """

    fs = FluidSynth()
    fs.midi_to_audio(in_fname, out_fname)

def playWAV(fname: str):
    """ Play the WAV file called fname through playsound library """

    playsound(fname)

def playWAVkivy(filename: str):
    """ Play the WAV file called filename through kivy SoundLoader """

    sound = SoundLoader.load(filename)
    if sound:
        sound.play()