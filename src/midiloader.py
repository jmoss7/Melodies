# IMPORTANT NOTE: This library/file does not accommodate for all bytes
# that can be found in a MIDI file. This library (as of now)
# only takes care of messages that will help build a Melody object. In the
# future, more functionality can be added so that it can work well with all
# bytes in all MIDI files (e.g. This file only works with MIDI files using a
# single track on channel 0 only

from melody import Melody
from note import Note
from mido import tempo2bpm
from general import *

CHUNK_TYPE_AND_LENGTH = 8
PROGRAM_CHANGE_STATUS = 192
NOTE_OFF_MIN_STATUS = 128
NOTE_OFF_MAX_STATUS = 143
NOTE_ON_MIN_STATUS = 144
NOTE_ON_MAX_STATUS = 159

# Meta Messages/Events
META_MSG = 255
SEQ_NBR_EVENT = 0
TEXT_EVENT = 1
COPYRIGHT_EVENT = 2
NAME_EVENT = 3
INSTR_NAME_EVENT = 4
LYRIC_EVENT = 5
MARKET_EVENT = 6
CUE_POINT_EVENT = 7
MIDI_CH_EVENT = 32
EOT_EVENT = 47
SET_TEMPO_EVENT = 81
SMPTE_OFF_EVENT = 84
TIME_SIG_EVENT = 88
KEY_SIG_EVENT = 89
SPECIAL_EVENT = 127

def getMelodyFromFile(fname: str):
    if len(fname) < 5:
        return

    if fname[len(fname)-4:] != ".mid":
        return

    blist, timings, options = loadFile(fname)

    if blist:
        return bytesToMelody(blist, timings, options)

def loadFile(fname: str):
    try:
        srcFile = open(fname, 'rb')
    except:
        return []

    byte_list = []  #
    noteDeltas = []  # Timing of notes
    unused = []  # Filled with bytes not specifically put into byte_list
    parameters = readHeader(srcFile)
    parameters["scale"] = 0
    parameters["tempo"] = -1  # -1 means use default bpm/tempo for melody
    parameters["time_sig_num"] = 4  # Assume 4/4 time signature by default
    parameters["time_sig_den"] = 4
    parameters["key"] = 0
    bytesLeft = True

    while bytesLeft:
        nextBytes = []
        i = 0
        isMeta = False

        while i < 3:
            curByte = srcFile.read(1)
            if not curByte:  # If end of file, stop reading bytes
                bytesLeft = False
                break

            b = int.from_bytes(curByte, "big")
            if b >= 128 or i > 0 or isMeta:
                # Do not pay attention to messages that start with value < 128
                if (NOTE_OFF_MIN_STATUS < b < NOTE_OFF_MAX_STATUS) and i == 0:
                    # Only focus on channel=0 note off messages
                    unused.append(b)
                else:
                    if b == NOTE_OFF_MIN_STATUS and i == 0 and not isMeta:
                        # Use last (up to) four unused bytes for delta time
                        noteDeltas.append(getVariableLength(unused))
                    elif b == META_MSG and i == 0:
                        isMeta = True

                    nextBytes.append(b)
                    i += 1
            else:
                unused.append(b)

        if bytesLeft or len(nextBytes) == 3:
            if isMeta:
                if nextBytes[1] == EOT_EVENT:
                    bytesLeft = False
                elif nextBytes[1] == SET_TEMPO_EVENT:
                    tempoBytes = srcFile.read(3)
                    tb = int.from_bytes(tempoBytes, "big")
                    parameters["tempo"] = int(tempo2bpm(tb))
                elif nextBytes[1] == TIME_SIG_EVENT:
                    n = int.from_bytes(srcFile.read(1), "big")
                    parameters["time_sig_num"] = n
                    dPow = int.from_bytes(srcFile.read(1), "big")
                    parameters["time_sig_den"] = 2 ** dPow
                    # For now, the other two bytes are not used
                    srcFile.read(2)
                elif nextBytes[1] == KEY_SIG_EVENT:
                    k = int.from_bytes(srcFile.read(1), "big", signed=True)
                    parameters["key"] = k
                    s = int.from_bytes(srcFile.read(1), "big")
                    parameters["scale"] = s
                else:
                    # For the messages that are not used, just read over it
                    srcFile.read(nextBytes[2])
            else:
                byte_list.append(nextBytes)

                unused.clear()

    srcFile.close()
    return byte_list, noteDeltas, parameters

def bytesToMelody(blist: List[List[int]], deltas: List[int], options: Dict):
    i = 0
    isTickPerBeats = False

    if options["scale"] == 0:
        scale = "major"
    else:
        scale = "minor"

    key = midiToKey(options["key"], scale)

    loadedMelody = Melody([], scale=scale, time_sig=(options["time_sig_num"],
                          options["time_sig_den"]), key_sig=key)

    if options["tempo"] != -1:
        loadedMelody.setBPM(options["tempo"])

    if options["divType"] == 0:
        isTickPerBeats = True

    curNote = Note(0, 0)

    for trio in blist:
        if trio[0] == PROGRAM_CHANGE_STATUS and trio[2] == 0:
            loadedMelody.setInstrument(trio[1])
        elif NOTE_ON_MIN_STATUS <= trio[0] <= NOTE_ON_MAX_STATUS:
            curNote.setMidiNumber(trio[1])
            curNote.setVelocity(trio[2])
        elif NOTE_OFF_MIN_STATUS <= trio[0] <= NOTE_OFF_MAX_STATUS:
            noteLen = 0
            if isTickPerBeats:
                noteLen = ticksToLength(deltas[i], options["divVal"],
                          int((1 / options["time_sig_den"]) * SMALLEST_NOTE))

            if noteLen > 0:
                curNote.setLength(noteLen)
                loadedMelody.addNote(curNote)
                curNote = Note(0, 0)

            i += 1

    loadedMelody.setOctave(determineOctave(loadedMelody.getNotes()),
                           transposeExisting=False)

    if isTickPerBeats:
        loadedMelody.generateMIDI(tpb=options["divVal"])
    else:
        loadedMelody.generateMIDI()

    return loadedMelody

def readHeader(fp):
    settings = {}

    fp.seek(0, 0)
    fp.read(CHUNK_TYPE_AND_LENGTH)

    frmt = int.from_bytes(fp.read(2), "big")
    settings["format"] = frmt

    numTracks = int.from_bytes(fp.read(2), "big")
    settings["numTracks"] = numTracks

    divType = int.from_bytes(fp.read(2), "big")
    if divType & 0x8000:
        settings["divType"] = 1
        settings["divVal"] = 0  # FIX: Later on, make this work as it should
    else:
        settings["divType"] = 0  # Ticks per beat
        settings["divVal"] = divType

    return settings

def getVariableLength(deltaBytes: List[int]):
    val = 0
    bank = deltaBytes.copy()
    if len(bank) > 4:
        l = len(bank)
        bank = bank[l-4:l]
    highestPow = len(bank) - 1

    for i in range(len(bank)):
        val += (bank[i] & 0x7F) << (highestPow * 7)
        highestPow -= 1

    return val

def midiToKey(val: int, scale: str):
    if scale == "major":
        midiKeys = {-7: "Cb", -6: "Gb", -5: "Db", -4: "Ab", -3: "Eb", -2: "Bb",
                    -1: "F", 0: "C", 1: "G", 2: "D", 3: "A", 4: "E", 5: "B",
                    6: "F#", 7: "C#"}
    else:
        midiKeys = {-7: "Ab", -6: "Eb", -5: "Bb", -4: "F", -3: "C", -2: "G",
                    -1: "D", 0: "A", 1: "E", 2: "B", 3: "F#", 4: "C#", 5: "G#",
                    6: "D#", 7: "A#"}

    return midiKeys[val]

def determineOctave(noteList: List[Note]):
    octaves = [0] * 10  # Octave -1 => Index 0, Octave 9 => Index 10

    for n in noteList:
        octaves[n.getOctave() + 1] += 1

    maxIdx = 0
    for i in range(10):
        if octaves[i] > octaves[maxIdx]:
            maxIdx = i

    return maxIdx - 1
