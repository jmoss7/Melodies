# Number of clock ticks for each beat (best if large and must be divisible by
# SMALLEST_NOTE (beat = 1/4))
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

def limiter(val: int):
    """ Caps val so that highest return value is 127 and lowest is 0 """

    if val > 127:
        return 127
    elif val < 0:
        return 0

    return val

def keyToMIDISig(key: str, scale: str):
    """ Takes a Melody or MelodyStack's key and its scale and returns
        the string stored in the MIDI MetaMessage for key signature """

    scale = scale.lower()
    key = key.capitalize()

    if "minor" in scale:
        end = 'm'
    else:
        end = ''

    return key + end