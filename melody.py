from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from instruments import *

# Macros
TICKS_PER_BEAT = 480  # Best if large and divisible by SMALLEST_NOTE (beat=1/4)
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

class Melody:
    def __init__(self, contents, instrument=0, bpm=120, scale="major",
                 time_sig=(4, 4), key_sig="C"):
        if not contents or not isinstance(contents, list):
            self.sequence = []
        else:
            self.sequence = contents

        self.length = sum([x.getLength() for x in contents])
        self.numNotes = len(contents)
        self.instrument = instrument
        self.bpm = bpm
        self.scale = scale
        self.timeSig = time_sig
        self.keySig = key_sig
        self.file = MidiFile()

    def __len__(self):
        return self.numNotes

    def __str__(self):
        if self.numNotes == 0:
            return "Empty Melody"

        header = "------------------------\n"
        header += "Instrument: {}\n".format(getInstrument(self.instrument))
        header += "------------------------\n"
        header += "Note | Length | Velocity\n------------------------\n"

        for elem in self.sequence:
            if elem.getName() == "Rest":
                header += " Rest "
            else:
                header += "{0:^5} ".format(elem.getName() + \
                                           str(elem.getOctave()))
            header += "{0:^8} ".format(elem.getLength())
            header += "{0:^9}\n".format(elem.getVelocity())

        return header

    def __repr__(self):
        return str(self)

    def getNotes(self):
        return self.sequence

    def getLength(self):
        return self.length

    def getMusicalNotes(self):
        return [x for x in self.sequence if x.getVelocity() != 0]

    def getScale(self):
        return self.scale

    def getKeySignature(self):
        return self.keySig

    def getTimeSignature(self):
        return self.timeSig

    def addNote(self, n):
        self.sequence.append(n)
        self.length += n.getLength()
        self.numNotes += 1

    def removeNote(self, idx):
        self.length -= self.sequence[idx].getLength()
        self.numNotes -= 1
        self.sequence.pop(idx)

    def generateMIDI(self):
        self.file.ticks_per_beat = TICKS_PER_BEAT
        track = MidiTrack()
        self.file.tracks.append(track)

        track.append(Message('program_change',program=self.instrument, time=0))
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))
        track.append(MetaMessage('time_signature', numerator=self.timeSig[0],
                                                denominator=self.timeSig[1]))

        for i in range(len(self)):
            noteLen = self.sequence[i].getLengthTime(TICKS_PER_BEAT)
            track.append(Message('note_on',
                                 note=self.sequence[i].getMidiNumber(),
                                 velocity=self.sequence[i].getVelocity(),
                                 time=0))

            track.append(Message('note_off',
                                 note=self.sequence[i].getMidiNumber(),
                                 velocity=64,
                                 time=noteLen))

    def saveMelodyAs(self, name):
        self.file.save(name)