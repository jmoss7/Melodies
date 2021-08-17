from typing import List, Tuple, Dict, TextIO

# Number of clock ticks for each beat (best if large and must be divisible by
# SMALLEST_NOTE (beat = 1/(denominator of the time signature))
TICKS_PER_BEAT = 480

SMALLEST_NOTE = 32  # 1/32 note is smallest note possible for Melodies

# Length of each Note (out of 1/32th note)
THIRTY_SECOND_NOTE = 1
SIXTEENTH_NOTE = 2
EIGHTH_NOTE = 4
QUARTER_NOTE = 8
HALF_NOTE = 16
WHOLE_NOTE = 32

# Dotted notes are length of regular note plus length of half of the note
DOTTED_SIXTEENTH_NOTE = SIXTEENTH_NOTE + THIRTY_SECOND_NOTE
DOTTED_EIGHTH_NOTE = EIGHTH_NOTE + SIXTEENTH_NOTE
DOTTED_QUARTER_NOTE = QUARTER_NOTE + EIGHTH_NOTE
DOTTED_HALF_NOTE = HALF_NOTE + QUARTER_NOTE
DOTTED_WHOLE_NOTE = WHOLE_NOTE + HALF_NOTE

MIN_BARS = 1
MAX_BARS = 8

def limiter(val: int, low: int = 0, high: int = 127):
    """ Caps val so that highest return value is high and lowest is low
        Note: This function is mainly used to make sure that MIDI numbers
        will be 8-bit, so by default the lower limit = 0 and the higher
        limit = 127 """

    if val > high:
        return high

    if val < low:
        return low

    return val

def keyToMIDISig(key: str, scale: str):
    """ Takes a Melody or MelodyStack's key and its scale and returns
        the string stored in the MIDI MetaMessage for key signature """

    scale = scale.lower()

    if "minor" in scale:
        end = 'm'
        key = key.lower()
        key = key.capitalize()
    else:
        key = sharpsToFlats(key)
        end = ''

    return key + end

def flatsToSharps(key: str):
    """ For this program, when storing data about a melody, keys are
        always defined by whole notes and sharps (no flats). So this
        function converts flat note to a sharp if applicable (e.g. C#->Db) """

    if len(key) == 2 and key[1].lower() == 'b':
        key = key.lower()
        key = key.capitalize()
        conversionDict = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#",
                          "Bb": "A#"}
        return conversionDict[key]

    return key

def sharpsToFlats(key: str):
    """ In certain situations (e.g. key signature message for MIDI), some
        sharps are not valid. Therefore, this function converts a sharp
        key to a flat key if applicable (e.g G#->Ab) """

    if len(key) == 2 and key[1].lower() == '#':
        key = key.lower()
        key = key.capitalize()
        conversionDict = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab",
                          "A#": "Bb"}
        return conversionDict[key]

    return key

def ticksToLength(ticks: int, timeRes: int, beatLength: int):
    return ticks // (timeRes // beatLength)
