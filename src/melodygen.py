from melody import Melody
from note import Note
from scales import generate_scale, get_random_scale
from instruments import *
from structures import *
from general import *

# Random Instrument Types
# (NP: Non-Percussion, NS: Non-FX, P: With Percussion, S: With FX)
# Random instrument from specific category
INSTRUMENT_WITH_CATEGORY = -1
# Random instrument without a specific category
INSTRUMENT_NP_NS_WITHOUT_CATEGORY = -2
INSTRUMENT_NP_S_WITHOUT_CATEGORY = -3
INSTRUMENT_P_S_WITHOUT_CATEGORY = -4

LOWEST_BPM = 20
HIGHEST_BPM = 180

def createMelody(instrument: int = INSTRUMENT_NP_NS_WITHOUT_CATEGORY,
                 instrument_cat: str = "", bpm: int = -1, scale: str = "",
                 octave: int = -1, time_sig: Tuple[int, int] = (4,4),
                 key_sig: str = "", bars: int = -1, makeEmpty: bool = False):
    """ Given an optional set of parameters, returns a Melody object based
        on random and/or specified characteristics """

    # instrument - MIDI number of instrument or type of random instrument
    # instrument_cat - Category of random instrument (if specified)
    # bpm - The beats per minute of the melody
    # scale - The scale that the melody is based on
    # octave - The octave that the melody is based on
    # time_sig - The time signature that the melody is played in
    # key_sig - The key that the melody is based on
    # bars - The number of bars/measures that the melody spans over
    # makeEmpty - Whether the melody should generate random notes or not

    if instrument < 0:
        randInstrument = chooseRandomInstrument(instrument, instrument_cat)
    else:
        randInstrument = instrument

    if bpm < LOWEST_BPM or bpm > HIGHEST_BPM:
        randBPM = random.randint(LOWEST_BPM, HIGHEST_BPM)
    else:
        randBPM = bpm

    if scale == "":
        randScale = get_random_scale()
    else:
        randScale = scale

    possibleOctaves = getSuitableOctaves(randInstrument)
    if octave in possibleOctaves:
        randOctave = octave
    elif octave != -2:
        if octave > possibleOctaves[-1]:
            randOctave = possibleOctaves[-1]
        else:
            randOctave = possibleOctaves[0]
    else:
        randOctave = random.choice(possibleOctaves)

    if key_sig == "":
        randKey = random.choice(["C", "C#", "D", "D#", "E", "F", "F#", "G",
                                 "G#", "A", "A#", "B"])
    else:
        randKey = flatsToSharps(key_sig)

    randMelody = Melody([], instrument=randInstrument, bpm=randBPM,
                        scale=randScale, octave=randOctave, time_sig=time_sig,
                        key_sig=randKey)

    if not makeEmpty:
        buildMelodyNotes(randMelody, bars)

    return randMelody

def chooseRandomInstrument(randType: int, category: str = ""):
    """ Given a random instrument type (see Random Instrument Types above)
        and a category to choose from (if applicable), return a random
        instrument number that applies to those specifications """

    if randType == INSTRUMENT_WITH_CATEGORY:
        return getRandomInstrumentFromType(category)

    if randType == INSTRUMENT_NP_NS_WITHOUT_CATEGORY:
        bank = getNonPercussionInstruments(includeSynthEffects=False)
        return getMIDINumber(random.choice(bank))

    if randType == INSTRUMENT_NP_S_WITHOUT_CATEGORY:
        bank = getNonPercussionInstruments()
        return getMIDINumber(random.choice(bank))

    if randType == INSTRUMENT_P_S_WITHOUT_CATEGORY:
        return getRandomInstrument()

    # If invalid random instrument type, just return 0
    return 0

def getSuitableOctaves(instrument):
    """ Based on a specific instrument, return a list of octaves (integers)
        that are within each instruments max and min note limits """

    minNote, maxNote = getInstrumentMinMax(getInstrument(instrument))

    smallestOctave = minNote // 12
    # If the minimum note is the first note of the octave, also include that
    # octave as a suitable one
    if minNote % 12 == 0:
        smallestOctave -= 1

    largestOctave = (maxNote // 12) - 1
    # If the maximum note is not the last note of the octave, do not include
    # that octave as a suitable one
    if maxNote not in [11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 127]:
        largestOctave -= 1

    # Return each octave between smallest and largest octave, inclusively
    # (with repeated numbers indicating higher probabilities)
    suitable = []
    for i in range(max(0, smallestOctave), min(8, largestOctave + 1)):
        suitable.append(i)

    return suitable

def buildMelodyNotes(m, bars):
    """ Given a melody object and the length of the melody in bars, fill
        the melody object with random notes based on its characteristics
        (octave, scale, key, etc.) """

    # Get the notes part of the scale specified in Melody object
    s = generate_scale(m.getKeySignature(), m.getScale(), m.getOctave())

    if bars < MIN_BARS or bars > MAX_BARS:
        bars = random.randint(MIN_BARS, MAX_BARS)

    # Get a random number of notes value between the number of bars (so
    # that there is roughly one note per bar) and SMALLEST_NOTE //
    # OTHER_NOTE (so that each note would be roughly OTHER_NOTE long)
    numNotes = random.randint(4, max(1, bars * (SMALLEST_NOTE //
                                                DOTTED_EIGHTH_NOTE)))
    seq = []
    # randomize notes in scale by choosing {numNotes} random notes
    for i in range(numNotes):
        seq.append(random.choice(s))

    # randomize length of each notes using getRandomStructure function
    lengths, barSpace = getBeatStructure(bars, numNotes)

    # add the random notes to generate the melody
    for i in range(numNotes):
        if seq[i] == -1:
            m.addNote(Note(0, lengths[i], vel=0))
        else:
            m.addNote(Note(seq[i], lengths[i]))

    if barSpace > 0:
        # Add rest just in case last note does not extend to end of bar
        m.addNote(Note(0, barSpace, vel=0))
