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
               "Synth Strings 1", "Synth Strings 2", "Choir Aahs",
               "Voice Oohs", "Synth Voice", "Orchestra Hit", "Trumpet",
               "Trombone", "Tuba", "Muted Trumpet", "French Horn",
               "Brass Section", "Synth Brass 1", "Synth Brass 2",
               "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe",
               "English Horn", "Bassoon", "Clarinet", "Piccolo", "Flute",
               "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi",
               "Whistle", "Ocarina", "Lead 1 (square)", "Lead 2 (sawtooth)",
               "Lead 3 (calliope)", "Lead 4 (chiff)", "Lead 5 (charang)",
               "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)",
               "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)",
               "Pad 4 (choir)", "Pad 5 (bowed)", "Pad 6 (metallic)",
               "Pad 7 (halo)", "Pad 8 (sweep)", "FX 1 (rain)",
               "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)",
               "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)",
               "FX 8 (sci-fi)", "Sitar", "Banjo", "Shamisen", "Koto",
               "Kalimba", "Bag pipe", "Fiddle", "Shanai", "Tinkle Bell",
               "Agogo", "Steel Drums", "Woodblock", "Taiko Drum",
               "Melodic Tom", "Synth Drum", "Reverse Cymbal",
               "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet",
               "Telephone Ring", "Helicopter", "Applause", "Gunshot"]

# The 'instrumentToMIDI' variable is a dictionary where each key represents
# an instrument name as a String and each value represents the MIDI number
# of that instrument (e.g. instrumentToMIDI["harmonica"] => 22)
instrumentToMIDI = {"acoustic grand piano": 0, "bright acoustic piano": 1,
                    "electric grand piano": 2, "honky-tonk piano": 3,
                    "electric piano 1": 4, "electric piano 2": 5,
                    "harpsichord": 6, "clavi": 7, "celesta": 8,
                    "glockenspiel": 9, "music box": 10, "vibraphone": 11,
                    "marimba": 12, "xylophone": 13, "tubular bells": 14,
                    "dulcimer": 15, "drawbar organ": 16,
                    "percussive organ": 17, "rock organ": 18,
                    "church organ": 19, "reed organ": 20, "accordion": 21,
                    "harmonica": 22, "tango accordion": 23,
                    "acoustic guitar (nylon)": 24,
                    "acoustic guitar (steel)": 25,
                    "electric guitar (jazz)": 26,
                    "electric guitar (clean)": 27,
                    "electric guitar (muted)": 28, "overdriven guitar": 29,
                    "distortion guitar": 30, "guitar harmonics": 31,
                    "acoustic bass": 32, "electric bass (finger)": 33,
                    "electric bass (pick)": 34, "fretless bass": 35,
                    "slap bass 1": 36, "slap bass 2": 37, "synth bass 1": 38,
                    "synth bass 2": 39, "violin": 40, "viola": 41, "cello": 42,
                    "contrabass": 43, "tremolo strings": 44,
                    "pizzicato strings": 45, "orchestral harp": 46,
                    "timpani": 47, "string ensemble 1": 48,
                    "string ensemble 2": 49, "synth strings 1": 50,
                    "synth strings 2": 51, "choir aahs": 52, "voice oohs": 53,
                    "synth voice": 54, "orchestra hit": 55, "trumpet": 56,
                    "trombone": 57, "tuba": 58, "muted trumpet": 59,
                    "french horn": 60, "brass section": 61,
                    "synth brass 1": 62, "synth brass 2": 63,
                    "soprano sax": 64, "alto sax": 65, "tenor sax": 66,
                    "baritone sax": 67, "oboe": 68, "english horn": 69,
                    "bassoon": 70, "clarinet": 71, "piccolo": 72, "flute": 73,
                    "recorder": 74, "pan flute": 75, "blown bottle": 76,
                    "shakuhachi": 77, "whistle": 78, "ocarina": 79,
                    "lead 1 (square)": 80, "lead 2 (sawtooth)": 81,
                    "lead 3 (calliope)": 82, "lead 4 (chiff)": 83,
                    "lead 5 (charang)": 84, "lead 6 (voice)": 85,
                    "lead 7 (fifths)": 86, "lead 8 (bass + lead)": 87,
                    "pad 1 (new age)": 88, "pad 2 (warm)": 89,
                    "pad 3 (polysynth)": 90, "pad 4 (choir)": 91,
                    "pad 5 (bowed)": 92, "pad 6 (metallic)": 93,
                    "pad 7 (halo)": 94, "pad 8 (sweep)": 95, "fx 1 (rain)": 96,
                    "fx 2 (soundtrack)": 97, "fx 3 (crystal)": 98,
                    "fx 4 (atmosphere)": 99, "fx 5 (brightness)": 100,
                    "fx 6 (goblins)": 101, "fx 7 (echoes)": 102,
                    "fx 8 (sci-fi)": 103, "sitar": 104, "banjo": 105,
                    "shamisen": 106, "koto": 107, "kalimba": 108,
                    "bag pipe": 109, "fiddle": 110, "shanai": 111,
                    "tinkle bell": 112, "agogo": 113, "steel drums": 114,
                    "woodblock": 115, "taiko Drum": 116, "melodic tom": 117,
                    "synth drum": 118, "reverse cymbal": 119,
                    "guitar fret noise": 120, "breath noise": 121,
                    "seashore": 122, "bird tweet": 123, "telephone ring": 124,
                    "helicopter": 125, "applause": 126, "gunshot": 127}

# The 'instrumentMinMax' variable is a dictionary where each key represents
# an instrument name as a String and each value represents the minimum and
# maximum MIDI note that can be played/heard by a certain instrument
# Notes
# 1) These values are based on listening tests performed by a 21 year old
# student on MacBook Air and may not be 100% accurate for all machines/people.
# 2) These were tested with note velocity being max (127)
# 3) Although some notes had higher maximums or minimums, accuracy of note was
# also taken into consideration when determining max or min note (aliasing)
instrumentMinMax = {"acoustic grand piano": (12, 108),
                    "bright acoustic piano": (12, 108),
                    "electric grand piano": (0, 108),
                    "honky-tonk piano": (12, 108),
                    "electric piano 1": (0, 108), "electric piano 2": (0, 127),
                    "harpsichord": (0, 127), "clavi": (0, 108),
                    "celesta": (0, 108), "glockenspiel": (0, 127),
                    "music box": (12, 125), "vibraphone": (0, 108),
                    "marimba": (0, 108), "xylophone": (0, 127),
                    "tubular bells": (0, 108), "dulcimer": (0, 108),
                    "drawbar organ": (24, 127), "percussive organ": (0, 108),
                    "rock organ": (0, 108), "church organ": (0, 96),
                    "reed organ": (0, 108), "accordion": (0, 108),
                    "harmonica": (0, 108), "tango accordion": (0, 108),
                    "acoustic guitar (nylon)": (0, 127),
                    "acoustic guitar (steel)": (0, 127),
                    "electric guitar (jazz)": (0, 96),
                    "electric guitar (clean)": (0, 127),
                    "electric guitar (muted)": (0, 127),
                    "overdriven guitar": (0, 108),
                    "distortion guitar": (0, 108), "guitar harmonics": (0, 85),
                    "acoustic bass": (0, 127),
                    "electric bass (finger)": (0, 84),
                    "electric bass (pick)": (0, 84), "fretless bass": (0, 84),
                    "slap bass 1": (0, 84), "slap bass 2": (0, 84),
                    "synth bass 1": (0, 127), "synth bass 2": (0, 127),
                    "violin": (0, 108), "viola": (0, 96), "cello": (0, 127),
                    "contrabass": (0, 81), "tremolo strings": (0, 127),
                    "pizzicato strings": (12, 108),
                    "orchestral harp": (0, 108), "timpani": (1, 127),
                    "string ensemble 1": (0, 127),
                    "string ensemble 2": (0, 127), "synth strings 1": (0, 127),
                    "synth strings 2": (0, 127), "choir aahs": (1, 96),
                    "voice oohs": (12, 96), "synth voice": (0, 127),
                    "orchestra hit": (0, 96), "trumpet": (0, 108),
                    "trombone": (0, 96), "tuba": (0, 72),
                    "muted trumpet": (0, 96), "french horn": (0, 96),
                    "brass section": (0, 96), "synth brass 1": (0, 127),
                    "synth brass 2": (0, 127), "soprano sax": (0, 127),
                    "alto sax": (0, 87), "tenor sax": (0, 109),
                    "baritone sax": (0, 109), "oboe": (1, 96),
                    "english horn": (0, 109), "bassoon": (0, 84),
                    "clarinet": (0, 119), "piccolo": (12, 115),
                    "flute": (0, 112), "recorder": (12, 116),
                    "pan flute": (12, 109), "blown bottle": (0, 107),
                    "shakuhachi": (12, 112), "whistle": (24, 117),
                    "ocarina": (0, 108), "lead 1 (square)": (0, 111),
                    "lead 2 (sawtooth)": (0, 111),
                    "lead 3 (calliope)": (0, 108), "lead 4 (chiff)": (0, 109),
                    "lead 5 (charang)": (0, 109), "lead 6 (voice)": (0, 113),
                    "lead 7 (fifths)": (0, 119),
                    "lead 8 (bass + lead)": (0, 111),
                    "pad 1 (new age)": (0, 112), "pad 2 (warm)": (12, 113),
                    "pad 3 (polysynth)": (0, 111), "pad 4 (choir)": (0, 112),
                    "pad 5 (bowed)": (0, 117), "pad 6 (metallic)": (12, 112),
                    "pad 7 (halo)": (12, 112), "pad 8 (sweep)": (8, 108),
                    "fx 1 (rain)": (0, 118), "fx 2 (soundtrack)": (0, 111),
                    "fx 3 (crystal)": (12, 113), "fx 4 (atmosphere)": (0, 115),
                    "fx 5 (brightness)": (0, 108), "fx 6 (goblins)": (0, 108),
                    "fx 7 (echoes)": (0, 96), "fx 8 (sci-fi)": (0, 115),
                    "sitar": (12, 108), "banjo": (0, 110),
                    "shamisen": (0, 114), "koto": (0, 109),
                    "kalimba": (0, 127), "bag pipe": (0, 101),
                    "fiddle": (12, 108), "shanai": (12, 103),
                    "tinkle bell": (12, 108), "agogo": (12, 108),
                    "steel drums": (12, 111), "woodblock": (0, 127),
                    "taiko Drum": (0, 127), "melodic tom": (0, 127),
                    "synth drum": (0, 127), "reverse cymbal": (0, 127),
                    "guitar fret noise": (0, 127), "breath noise": (0, 127),
                    "seashore": (0, 127), "bird tweet": (0, 127),
                    "telephone ring": (0, 127), "helicopter": (0, 127),
                    "applause": (0, 127), "gunshot": (0, 127)}

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

def getInstrument(nbr: int):
    """ Returns the instrument name of the MIDI # given """

    return instruments[nbr]

def getMIDINumber(instrument: str):
    """ Returns the MIDI number of the instrument name given"""

    return instrumentToMIDI[instrument.lower()]

def getInstrumentTypes(sortByLetter: bool = False):
    """ Returns the list of categories(types) of instruments available """

    cats = list(categories.keys())

    if sortByLetter:
        return sorted(cats)

    return cats

def getAllInstruments(sortByLetter: bool = False):
    """ Returns the list of all the instrument names available"""

    if sortByLetter:
        return sorted(instruments)

    return instruments

def getNonPercussionInstruments(includeSynthEffects: bool = True):
    """ Returns the list of non-percussion instrument names available
        (Note: If the user does not want to include synth effects, the
        optional paramater 'includeSynthEffects' should be set to False
        during function call """

    nonPercussion = instruments[:96] + instruments[104:112]
    if includeSynthEffects:
        nonPercussion += instruments[96:104]

    return nonPercussion

def getCategoryFromInstrument(instrument):
    """ Returns the category of a given instrument where 'instrument' can
        be either the MIDI number of the instrument or the name of the
        instrument """

    if isinstance(instrument, str):
        val = instrumentToMIDI[instrument]
    else:
        val = instrument

    # Each category has eight instruments, so we can just use integer
    # division to grab the index and use the list of instrument types
    return ["piano", "chromatic percussion", "organ", "guitar", "bass",
            "strings", "ensemble", "brass", "reed", "pipe", "synth lead",
            "synth pad", "synth effects", "ethnic", "percussive",
            "sound effects"][(val // 8)]

def getInstrumentsofType(category: str):
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

    return random.randint(0, 127)

def getRandomInstrumentFromType(category: str):
    """ Returns the number of a random instrument that falls under the category
        given by the parameter 'category'. If category does not exist, return
        0 (Acoustic Grand Piano) """

    key = category.lower()
    if categories.get(key, False):
        return random.choice(categories[key])

    return 0

def getInstrumentMinMax(instrument: str):
    """ Returns a tuple representing the minimum (t[0]) and maximum (t[1])
        MIDI notes that parameter instrument can play """

    return instrumentMinMax[instrument.lower()]
