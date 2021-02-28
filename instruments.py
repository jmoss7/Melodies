import random

# The 'instruments' variable is an array where the value at index i represents
# the MIDI number for an instrument (e.g instrument #16 -> Drawbar Organ)
instruments = ["Acoustic Grand Piano", "Bright Acoustic Piano",
               "Electric Grand Piano", "Honky-tonk Piano", "Electric Piano 1",
               "Electric Piano 2", "Harpsichord", "Clavi", "Celesta",
               "Glockenspiel", "Music Box", "Vibraphone", "Marimba",
               "Xylophone", "Tubular Bells", "Dulcimer", "Drawbar Organ",
               "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ",
               "Accordion", "Harmonica", "Tango Accordion",
               "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)",
               "Electric Guitar (jazz)", "Electric Guitar (clean)",
               "Electric Guitar (muted)", "Overdriven Guitar",
               "Distortion Guitar", "Guitar Harmonics", "Acoustic Bass",
               "Electric Bass (finger)", "Electric Bass (pick)",
               "Fretless Bass", "Slap Bass 1", "Slap Bass 2", "Synth Bass 1",
               "Synth Bass 2", "Violin", "Viola", "Cello", "Contrabass",
               "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp",
               "Timpani", "String Ensemble 1", "String Ensemble 2",
               "Synth Strings 1", "Synth Strings 2", "Choir Aahs", "Voice Oohs",
               "Synth Voice", "Orchestra Hit", "Trumpet", "Trombone", "Tuba",
               "Muted Trumpet", "French Horn", "Brass Section",
               "Synth Brass 1", "Synth Brass 2", "Soprano Sax", "Alto Sax",
               "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", "Bassoon",
               "Clarinet", "Piccolo", "Flute", "Recorder", "Pan Flute",
               "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina",
               "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)",
               "Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)",
               "Lead 7 (fifths)", "Lead 8 (bass + lead)", "Pad 1 (new age)",
               "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)",
               "Pad 5 (bowed)", "Pad 6 (metallic)", "Pad 7 (halo)",
               "Pad 8 (sweep)", "FX 1 (rain)", "FX 2 (soundtrack)",
               "FX 3 (crystal)", "FX 4 (atmosphere)", "FX 5 (brightness)",
               "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)", "Sitar",
               "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle",
               "Shanai", "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock",
               "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal",
               "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet",
               "Telephone Ring", "Helicopter", "Applause", "Gunshot"]

# The 'categories' variable is a dictionary where each key-value pair
# represents a category of instruments and the list of MIDI #'s for the
# instruments in that category
categories = {"piano": [0, 1, 2, 3, 4, 5, 6, 7],
              "chromatic percussion": [8, 9, 10, 11, 12, 13, 14, 15],
              "organ": [16, 17, 18, 19, 20, 21, 22, 23],
              "guitar": [24, 25, 26, 27, 28, 29, 30, 31],
              "bass": [32, 33, 34, 35, 36, 37, 38, 39],
              "strings": [40, 41, 42, 43, 44, 45, 46, 47],
              "ensemble": [48, 49, 50, 51, 52, 53, 54, 55],
              "brass": [56, 57, 58, 59, 60, 61, 62, 63],
              "reed": [64, 65, 66, 67, 68, 69, 70, 71],
              "pipe": [72, 73, 74, 75, 76, 77, 78, 79],
              "synth lead": [80, 81, 82, 83, 84, 85, 86, 87],
              "synth pad": [88, 89, 90, 91, 92, 93, 94, 95],
              "synth effects": [96, 97, 98, 99, 100, 101, 102, 103],
              "ethnic": [104, 105, 106, 107, 108, 109, 110, 111],
              "percussive": [112, 113, 114, 115, 116, 117, 118, 119],
              "sound effects": [120, 121, 122, 123, 124, 125, 126, 127]}

def getInstrument(nbr):
    """ Returns the instrument name of the MIDI # given """

    return instruments[nbr]

def getInstrumentTypes():
    """ Returns the list of categories(types) of instruments available """

    return list(categories.keys())

def getAllInstruments():
    """ Returns the list of all the instrument names available"""

    return instruments

def getNonPercussionInstruments(includeSynthEffects=True):
    """ Returns the list of non-percussion instrument names available
        (Note: If the user does not want to include synth effects, the
        optional paramater 'includeSynthEffects' should be set to False
        during function call """

    nonPercussion = instruments[:96] + instruments[104:112]
    if includeSynthEffects:
        nonPercussion += instruments[96:104]

    return nonPercussion

def getInstrumentsofType(category):
    """ Returns the list of instruments that fall under the category given
        by the parameter 'category'. If category does not exist, return empty
        list """

    key = category.lower()
    if categories.get(key, False):
        return categories[key]

    return []

def getRandomInstrument():
    """ Returns the number of any random instrument out of the 128 possible
        instruments """
    return instruments[random.randint(0, 127)]

def getRandomInstrumentFromType(category):
    """ Returns the number of a random instrument that falls under the category
        given by the parameter 'category'. If category does not exist, return
        0 (Acoustic Grand Piano) """

    key = category.lower()
    if categories.get(key, False):
        return categories[key][random.randint(0, len(categories[key]) - 1)]

    return 0
