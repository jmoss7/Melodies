from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from instruments import getInstrument as getInstrumentName
from general import *
import scales
from note import Note
from typing import Tuple, List

# Below are the indices in a track that specific messages will appear
NAME_MSG_IDX = 0  # Should always be first message in track
BPM_MSG_IDX = 1
TIME_SIG_MSG_IDX = 2
KEY_SIG_MSG_IDX = 3
INSTRUMENT_MSG_IDX = 4  # Should always be last message in track before notes
FIRST_NOTE_MSG_IDX = 5  # Should always be +1 of last setup message

class Melody:
    # Dunder methods (__method__)
    def __init__(self, contents: List[Note], instrument: int = 0,
                 bpm: int = 120, scale: str = "major", octave: int = 4,
                 time_sig: Tuple[int, int] = (4, 4), key_sig: str = "C"):
        """ Constructs a Melody object, which contains the characteristics
            of a melody and its MIDI file """

        if not contents:
            self.sequence = []
        else:
            self.sequence = []
            for n in contents:
                self.sequence.append(n.duplicate())

        self.length = sum([len(x) for x in contents])

        self.numNotes = len(contents)
        self.octave = octave
        self.instrument = instrument
        self.bpm = bpm
        self.scale = scale
        self.timeSig = time_sig
        self.keySig = key_sig
        self.file = MidiFile()  # MIDI file for melody
        self.modified = True  # Flag for whether MIDI file is outdated

    def __len__(self):
        """ Returns the length of the melody in units SMALLEST_NOTE (1/32) """

        return self.length

    def __str__(self):
        if self.numNotes == 0:
            return "Empty Melody"

        header = "------------------------\n"
        header += "BPM: {}, Time Signature: {}/{}\n".format(self.bpm,
                                                            self.timeSig[0],
                                                            self.timeSig[1])
        header += "Key: {}, Scale: {}\n".format(self.keySig,
                                                self.scale.capitalize())
        header += "Length: {} ({} measures), # of Notes: {}\n".format(
                  self.length, self.length // SMALLEST_NOTE, self.numNotes)
        header += "------------------------\n"
        header += "Instrument: {}\n".format(getInstrumentName(
                                            self.instrument))
        header += "------------------------\n"
        header += " Note  | Length | Velocity\n------------------------\n"

        for elem in self.sequence:
            if elem.getName() == "Rest":
                header += " Rest   "
            else:
                header += "{0:^7} ".format(elem.getName() + \
                                           str(elem.getOctave()))
            header += "{0:^8} ".format(len(elem))
            header += "{0:^9}\n".format(elem.getVelocity())

        header += "Total Length: {}".format(self.length)

        return header

    def __repr__(self):
        return str(self)

    # GET and SET functions
    def getNotes(self):
        """ Returns the array of Note objects associated with melody """

        return self.sequence

    def getNumNotes(self):
        """ Returns the number of notes in the melody (including rests) """

        return self.numNotes

    def getInstrument(self):
        """ Returns the MIDI number of the instrument used in melody """

        return self.instrument

    def getMusicalNotes(self):
        """ Returns the array of Note objects in melody that are not rests """

        return [x for x in self.sequence if x.getVelocity() != 0]

    def getOctave(self):
        """ Returns the octave that this melody's notes are based on """

        return self.octave

    def getScale(self):
        """ Returns the musical scale associated with the melody """

        return self.scale

    def getKeySignature(self):
        """ Returns the key of the melody (e.g. D# not D#m) """

        return self.keySig

    def getTimeSignature(self):
        """ Returns the time signature of the melody """

        return self.timeSig

    def getBPM(self):
        """ Returns the beats per minute of the melody """

        return self.bpm

    def setInstrument(self, newInstrument: int):
        """ Sets the MIDI number of the instrument used in melody """

        self.instrument = newInstrument
        self.modified = True

    def setOctave(self, newOctave: int, transposeExisting: bool = True):
        """ Sets the octave that the melody's notes are based on and
            if the melody already has notes, transposes the notes
            based on that new octave """

        if self.length > 0:
            if self.octave == newOctave:
                return

            if transposeExisting:
                for n in self.sequence:
                    # Increase (or decrease) octave to newOctave
                    n.incrementOctave(newOctave - self.octave)

        self.octave = newOctave
        self.modified = True

    def setScale(self, newScale: str, transposeExisting: bool = True):
        """ Sets the musical scale asociated with the melody and if the
            melody already contains notes, transposes the notes to the
            new musical scale (if possible) """

        if self.length > 0:
            if self.scale == newScale:
                return

            if transposeExisting:
                oldScaleKeys = scales.generate_scale(
                    self.keySig, self.scale, self.octave)
                newScaleKeys = scales.generate_scale(
                    self.keySig, newScale, self.octave)

                if len(oldScaleKeys) != len(newScaleKeys):
                    # For now, this function only works when scales have same
                    # number of notes
                    return

                # Get the difference between the new MIDI number and the old
                diff = [newScaleKeys[i] - oldScaleKeys[i]
                        for i in range(len(oldScaleKeys))]

                oldDict = {}

                for i in range(len(oldScaleKeys)):
                    oldDict[oldScaleKeys[i]] = i

                for n in self.sequence:
                    # Get the index of the note in its original scale
                    try:
                        diffIdx = oldDict[n.getMidiNumber()]
                        n.semitoneChange(diff[diffIdx])
                    except:
                        pass

        self.scale = newScale
        self.modified = True

    def setKeySignature(self, newKeySig: str, transposeExisting: bool = True):
        """ Sets the key of the melody and if the melody already contains
            notes, transposes the notes to the new key """

        if self.length > 0:
            if self.keySig == newKeySig:
                return

            if transposeExisting:
                sharpKey = flatsToSharps(newKeySig)
                allKeys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",
                           "A", "A#", "B"]

                # delta is the amount of semitones up or down the new key is
                # from the old key (Note: This will always assume a key change
                # will be from a lower key to a higher key, so to key change
                # down from C to B, user must first change key and then lower
                # the octave by 1
                delta = allKeys.index(sharpKey) - allKeys.index(self.keySig)

                for n in self.sequence:
                    n.semitoneChange(delta)

        self.keySig = newKeySig
        self.modified = True

    def setTimeSignature(self, newTimeSig: Tuple[int, int]):
        """ Sets the time signature of the melody """

        self.timeSig = newTimeSig
        self.modified = True

    def setBPM(self, newBPM: int):
        """ Sets the BPM of the melody """

        self.bpm = newBPM
        self.modified = True

    def setAsModified(self):
        """ Sets the melody as being modified """

        self.modified = True

    # Additional functions
    def addNote(self, n: Note):
        """ Appends a Note object to the melody """
        self.sequence.append(n)
        self.length += len(n)
        self.numNotes += 1
        self.modified = True

    def removeNote(self, idx: int):
        """ Removes the Note object at index idx of the melody and returns
            that note object """

        self.length -= len(self.sequence[idx])
        self.numNotes -= 1
        n = self.sequence.pop(idx)
        self.modified = True
        return n

    def generateMIDI(self, tpb: int = TICKS_PER_BEAT):
        """ Build the MIDI file based on mido library specifications """

        if len(self.file.tracks) > 0:  # If this has been generated before
            if not self.modified:  # If melody has not been modified, leave it
                return

            self.file.tracks.clear()
        else:
            self.file.ticks_per_beat = tpb

        track = MidiTrack()  # Track to hold a single melody
        self.file.tracks.append(track)

        # Tell MIDI file to set the name of the track to 'Made w/ Melodies'
        track.append(MetaMessage('track_name', name='Made w/ Melodies'))

        # Tell MIDI file to set tempo to BPM (must convert self.bpm to tempo)
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))

        # Tell MIDI file what time signature to play melody at
        track.append(MetaMessage('time_signature', numerator=self.timeSig[0],
                                                denominator=self.timeSig[1]))

        # Tell MIDI file which key signature melody is in
        track.append(MetaMessage('key_signature',
                                 key=keyToMIDISig(self.keySig, self.scale)))

        # Tell MIDI file to set instrument to self.instrument
        track.append(Message('program_change',program=self.instrument, time=0))

        for i in range(self.numNotes):
            noteLen = self.sequence[i].getLengthTime(self.file.ticks_per_beat,
                      int((1 / self.timeSig[1]) * SMALLEST_NOTE))

            # Tell MIDI file to play note right after previous note
            track.append(Message('note_on',
                                 note=self.sequence[i].getMidiNumber(),
                                 velocity=self.sequence[i].getVelocity(),
                                 time=0))

            # Tell MIDI file to stop playing note after noteLen time
            track.append(Message('note_off',
                                 note=self.sequence[i].getMidiNumber(),
                                 velocity=64,
                                 time=noteLen))

        self.modified = False

    def saveMelodyAs(self, name: str):
        """ Save the MIDI file in the program's directory as name """

        if self.modified:
            self.generateMIDI()

        self.file.save(name)

    def duplicate(self):
        """ Create a copy of this Melody object """

        return Melody(self.sequence, instrument=self.instrument, bpm=self.bpm,
                      scale=self.scale, time_sig=self.timeSig,
                      key_sig=self.keySig)

    def swapSegments(self, ref, swapPos):
        """ Given a reference melody, swap the notes starting from position
            swapPos in this melody with the notes starting from position
            swapPos in the melody ref (position refers to the number of
            SMALLEST_NOTE lengths) """

        if not(isinstance(ref, Melody)):
            # If reference melody is not of type melody, do not do anything
            return

        if len(ref) != len(self):
            # If the length of this melody is not exactly the length of the
            # reference melody, do not do anything
            return

        if swapPos < 0 or swapPos > self.length:
            # If the swap position is out of bounds with the note sequence, do
            # not do anything
            return

        selfCurPos, refCurPos = 0, 0
        selfIdx, refIdx = 0, 0

        # Set selfIdx and refIdx to the index of the first note to swap in
        # their respective melodies
        while selfCurPos < swapPos or refCurPos < swapPos:
            if selfCurPos < swapPos:
                selfCurPos += len(self.sequence[selfIdx])
                selfIdx += 1

            if refCurPos < swapPos:
                refCurPos += len(ref.sequence[refIdx])
                refIdx += 1

        # If selfCurPos > swapPos, that means that the swap position is in
        # the middle of a note. Cut the note at that section and make the
        # attribute changes to the Melody object
        if selfCurPos != swapPos:
            noteToChange = self.sequence[selfIdx-1]
            originalLength = len(noteToChange)
            extraLength = selfCurPos - swapPos
            noteToChange.setLength(originalLength - extraLength)
            splicedNote = noteToChange.duplicate()
            splicedNote.setLength(extraLength)
            self.sequence.insert(selfIdx, splicedNote)
            self.numNotes += 1

        # Do the same as above but with reference melody
        if refCurPos != swapPos:

            noteToChange = ref.sequence[refIdx-1]
            originalLength = len(noteToChange)
            extraLength = refCurPos - swapPos
            noteToChange.setLength(originalLength - extraLength)
            splicedNote = noteToChange.duplicate()
            splicedNote.setLength(extraLength)
            ref.sequence.insert(refIdx, splicedNote)
            ref.numNotes += 1

        # Save number of notes from selfIdx to end of sequence now since array
        # will be modified during while loop
        selfNotesToSwap = self.numNotes - selfIdx
        refNotesToSwap = ref.numNotes - refIdx

        while selfNotesToSwap > 0 or refNotesToSwap > 0:
            # Remove a note from one melody and add it to the end of the other
            if selfNotesToSwap > 0:
                noteFromSelf = self.removeNote(selfIdx)
                ref.addNote(noteFromSelf)
                selfNotesToSwap -= 1

            if refNotesToSwap > 0:
                noteFromRef = ref.removeNote(refIdx)
                self.addNote(noteFromRef)
                refNotesToSwap -= 1

        self.modified = True
        ref.modified = True

    def loop(self, numLoops: int):
        """ Loops a melody's notes numLoops amount of times """

        if self.length > 0 and numLoops > 0:
            addedNotes = self.sequence * numLoops
            addedLength = self.length * numLoops

            self.sequence += addedNotes
            self.length += addedLength
            self.numNotes = len(self.sequence)
            self.modified = True
