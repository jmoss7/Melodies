import global_vars
import subprocess

from kivy.core.audio import SoundLoader

def playMIDI(fname: str):
    """ Play the MIDI file called fname through FluidSynth """

    # This code takes inspiration from the midi2audio python library
    soundFont = '../support-files/req/melodies.sf2'
    try:
        subprocess.call(['fluidsynth', '-i', soundFont, fname, '-r', "44100"])
    except:
        print("There was an error while running fluidsynth. Check error "
              + "statement above for more information.")
        exit(1)

def midiToWAV(in_fname: str, out_fname: str):
    """ Convert the MIDI file called in_fname to the WAV file
        called out_fname """

    # This code takes inspiration from the midi2audio python library
    soundFont = '../support-files/req/melodies.sf2'
    try:
        subprocess.call(['fluidsynth', '-ni', soundFont, in_fname, '-F',
                         out_fname, '-r', "44100"])
    except:
        print("There was an error while running fluidsynth. Check error "
              + "statement above for more information.")
        exit(1)

def playWAVkivy(filename: str):
    """ Play the WAV file called filename through kivy SoundLoader """

    if global_vars.soundPlayer:
        if str(global_vars.soundPlayer.state) == "play":
            global_vars.soundPlayer.stop()

    global_vars.soundPlayer = SoundLoader.load(filename)
    if global_vars.soundPlayer:
        global_vars.soundPlayer.play()