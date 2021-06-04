import global_vars
from midi2audio import FluidSynth
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

def playWAVkivy(filename: str):
    """ Play the WAV file called filename through kivy SoundLoader """

    if str(global_vars.soundPlayer) == "play":
        global_vars.soundPlayer.stop()

    global_vars.soundPlayer = SoundLoader.load(filename)
    if global_vars.soundPlayer:
        global_vars.soundPlayer.play()