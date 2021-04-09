from melody import *

class MelodyStack:
    # Dunder methods (__method__)
    def __init__(self, bpm=120, time_sig=(4, 4), key_sig="C", scale="major",
                 allStartSameTime=True):
        """ Constructs a MelodyStack object, which is an array of melodies.
            The allStartSameTime boolean determines whether all the tracks in
            the MIDI must start at the same time or if the melodies can start
            at any time (see Melody class for melody characteristics) """

        if allStartSameTime:
            ft = 1
        else:
            ft = 2

        self.file = MidiFile(type=ft)  # MIDI file (.mid)
        self.subMelodies = []  # Array of melodies representing each Melody
        # object in the melody stack

        self.bpm = bpm  # BPM of the melody stack
        self.time_sig = time_sig  # Time signature of the melody stack
        self.key_sig = key_sig  # Key signature of the melody stack
        self.scale = scale  # Musical scale of the melody stack
        self.tracksFilled = 0  # Number of tracks with a melody inside them
        self.numberOfTracks = 8  # Total number of tracks (default: 8)

        self.file.ticks_per_beat = TICKS_PER_BEAT  # see melody.py

        for i in range(self.numberOfTracks):
            # Initialize arrays
            self.subMelodies.append(Melody([], bpm=bpm, scale=scale,
                                           time_sig=time_sig,
                                           key_sig=key_sig))
            self.file.tracks.append(MidiTrack())
            self.file.tracks[i].name = "Track {}".format(i)

    def __len__(self):
        """ Returns the length of the longest melody in the melody stack """

        return max([len(x) for x in self.subMelodies])

    def __str__(self):
        header = "\n------------------------\n"
        header += "BPM: {}, Time Signature: {}/{}, Key Signature: {}\n".format(
                    self.bpm, self.time_sig[0], self.time_sig[1], self.key_sig)
        header += "------------------------"

        if len(self) == 0:
            return header + "\nEmpty Melody Stack"

        body = ""
        count = self.tracksFilled

        for i in range(len(self.subMelodies)):
            if len(self.subMelodies[i]) == 0:
                if count == 0:
                    break
            else:
                body += "\n{}\n".format(self.file.tracks[i].name)
                body += "Instrument: {}\n".format(getInstrumentName(
                        self.subMelodies[i].getInstrument()))
                body += "------------------------\n"
                body += "Note | Length | Velocity\n------------------------\n"

                for elem in self.subMelodies[i].getNotes():
                    if elem.getName() == "Rest":
                        body += " Rest "
                    else:
                        body += "{0:^5} ".format(elem.getName() + \
                                                   str(elem.getOctave()))
                    body += "{0:^8} ".format(len(elem))
                    body += "{0:^9}\n".format(elem.getVelocity())

                body += "------------------------"

                count -= 1

        return header + body

    def __repr__(self):
        return str(self)

    # GET and SET functions
    def getNotes(self):
        """ Returns an array of arrays of Note objects containing the notes
            in each melody in the melody stack """

        return [x.getNotes() for x in self.subMelodies]

    def getScale(self):
        """ Returns the scale that the melodies in the stack are based on """

        return self.scale

    def getKeySignature(self):
        """ Returns the key of the melody stack """

        return self.key_sig

    def getTimeSignature(self):
        """ Returns the time signature of the melody stack """

        return self.time_sig

    def getBPM(self):
        """ Returns the beats per minute of the melody stack """

        return self.bpm

    def numberOfFilledTracks(self):
        """ Returns the number of tracks in the melody stack that contain
            melodies inside of them """

        return self.tracksFilled

    def totalTracks(self):
        """ Returns the total number of tracks in the melody stack """

        return self.numberOfTracks

    def setScale(self, newScale: str):
        """ Set the scale that the melodies in the melody stack are based
            on """

        self.scale = newScale

        for i in range(self.numberOfTracks):
            self.subMelodies[i].setScale(newScale)
            if len(self.file.tracks[i]) > 0:
                self.file.tracks[i] = self.file.tracks[i][:FIRST_NOTE_MSG_IDX]
                self.rebuildMelodyTrack(i)

    def setKeySignature(self, newKeySig: str):
        """ Set the key signature of the melody stack """
        self.key_sig = newKeySig

        for i in range(self.numberOfTracks):
            self.subMelodies[i].setKeySignature(newKeySig)
            if len(self.file.tracks[i]) > 0:
                self.file.tracks[i] = self.file.tracks[i][:FIRST_NOTE_MSG_IDX]
                self.file.tracks[i][KEY_SIG_MSG_IDX] = MetaMessage(
                    'key_signature', key=keyToMIDISig(newKeySig, self.scale))
                self.rebuildMelodyTrack(i)

    def setTimeSignature(self, newTimeSig: (int, int)):
        """ Set the time signature of the melody stack """

        self.time_sig = newTimeSig

        for i in range(self.numberOfTracks):
            self.subMelodies[i].setTimeSignature(newTimeSig)
            if len(self.file.tracks[i]) > 0:
                self.file.tracks[i][TIME_SIG_MSG_IDX] = MetaMessage(
                    'time_signature', numerator=newTimeSig[0],
                    denominator=newTimeSig[1])

    def setBPM(self, newBPM: int):
        """ Set the BPM of the melody stack """

        self.bpm = newBPM

        for i in range(self.numberOfTracks):
            self.subMelodies[i].setBPM(newBPM)
            if len(self.file.tracks[i]) > 0:
                self.file.tracks[i][BPM_MSG_IDX] = MetaMessage('set_tempo',
                                                tempo=bpm2tempo(self.bpm))

    # Additional functions
    def adjustMelodyForStack(self, newMelody: Melody):
        """ Change a melody to have characteristics suitable for the
            melody stack """

        adjusted = newMelody.duplicate()

        if adjusted.getScale() != self.scale:
            adjusted.setScale(self.scale)

        if adjusted.getTimeSignature() != self.time_sig:
            adjusted.setTimeSignature(self.time_sig)

        if adjusted.getKeySignature() != self.key_sig:
            adjusted.setKeySignature(self.key_sig)

        return adjusted

    def addMelody(self, trackNbr: int, newMelody: Melody):
        """ Adds the Melody object newMelody to the melody stack at index
            trackNbr, regardless of whether there is an existing Melody
            object present in that track or not """

        if trackNbr >= self.numberOfTracks or trackNbr < 0:
            # Should return error, but for now
            return

        self.subMelodies[trackNbr] = self.adjustMelodyForStack(newMelody)

        curTrack = self.file.tracks[trackNbr]

        if len(curTrack) == 0:
            # If this track was previously empty
            self.tracksFilled += 1
            curTrack.append(Message('program_change',
                                    program=newMelody.getInstrument(),
                                    time=0))
            curTrack.append(MetaMessage('set_tempo',
                                        tempo=bpm2tempo(self.bpm)))
            curTrack.append(MetaMessage('time_signature',
                                        numerator=self.time_sig[0],
                                        denominator=self.time_sig[1]))
            curTrack.append(MetaMessage('key_signature',
                                        key=keyToMIDISig(self.key_sig,
                                                         self.scale)))
        else:
            # Keep the original setup messages (excluding instrument),
            # set the correct instrument message, and append the
            # melody's notes
            curTrack = curTrack[1:FIRST_NOTE_MSG_IDX]
            curTrack.insert(0, Message('program_change',
                            program=newMelody.getInstrument(),
                            time=0))

        for i in range(newMelody.getNumNotes()):
            noteLen = newMelody.sequence[i].getLengthTime(TICKS_PER_BEAT)
            curTrack.append(Message('note_on',
                            note=newMelody.sequence[i].getMidiNumber(),
                            velocity=newMelody.sequence[i].getVelocity(),
                            time=0))

            curTrack.append(Message('note_off',
                            note=newMelody.sequence[i].getMidiNumber(),
                            velocity=64,
                            time=noteLen))

    def deleteMelody(self, trackNbr: int):
        """ If it exists, clears the contents of the track at index trackNbr
            while keeping the MidiTrack object """

        if trackNbr >= self.numberOfTracks or trackNbr < 0:
            # To prevent out of bounds error
            return

        # If not an empty melody
        if len(self.subMelodies[trackNbr]) > 0:
            self.subMelodies[trackNbr] = (Melody([], bpm=self.bpm,
                                                 scale=self.scale,
                                                 time_sig=self.time_sig,
                                                 key_sig=self.key_sig))
            oldTrack = self.file.tracks[trackNbr]
            self.file.tracks[trackNbr] = oldTrack[:FIRST_NOTE_MSG_IDX]
            self.tracksFilled -= 1

    def moveMelodies(self, srcNbr: int, destNbr: int):
        """ Takes the track at index srcNbr and swaps the position of the
            track with the track at index destNbr """

        if (max(srcNbr, destNbr) >= self.numberOfTracks
                or min(srcNbr, destNbr) < 0):
            # Don't try to access out of bounds indices
            return

        # Swap the Melody object at index srcNbr with object at index destNbr
        self.subMelodies[srcNbr], self.subMelodies[destNbr] = (
            self.subMelodies[destNbr], self.subMelodies[srcNbr])

        # Swap MidiTrack object at index srcNbr with object at index destNbr
        self.file.tracks[srcNbr], self.file.tracks[destNbr] = (
            self.file.tracks[destNbr], self.file.tracks[srcNbr]
        )

    def saveMelodyStackAs(self, name: str):
        """ Saves the melody stack to a MIDI file called name """
        self.file.save(name)

    def separateTracks(self):
        """ Returns an array of two arrays: one being the Melody objects
            that make up the melody stack and the other being the MidiTrack
            corresponding to each melody """

        return [self.subMelodies, self.file.tracks]

    def rebuildMelodyTrack(self, trackNbr: int):
        """ Rebuilds the track at trackNbr by adding note messages based
            on its corresponding melody (assuming track is not empty
            already) """

        if trackNbr >= self.numberOfTracks or trackNbr < 0:
            # Do not rebuild track with out of bounds index
            return

        if len(self.subMelodies[trackNbr]) > 0:
            newMelody = self.subMelodies[trackNbr]
            setupMessages = self.file.tracks[trackNbr][:FIRST_NOTE_MSG_IDX]
            self.file.tracks[trackNbr] = setupMessages

            for i in range(newMelody.getNumNotes()):
                noteLen = newMelody.sequence[i].getLengthTime(
                    TICKS_PER_BEAT)
                self.file.tracks[trackNbr].append(Message('note_on',
                            note=newMelody.sequence[i].getMidiNumber(),
                            velocity=newMelody.sequence[i].getVelocity(),
                            time=0))

                self.file.tracks[trackNbr].append(Message('note_off',
                            note=newMelody.sequence[i].getMidiNumber(),
                            velocity=64,
                            time=noteLen))

    def getSpecificMelody(self, trackNbr: int):
        """ Returns a specific melody associated with the track at trackNbr """

        if trackNbr >= self.numberOfTracks or trackNbr < 0:
            # Return None if trackNbr is not within bounds
            return None

        return self.subMelodies[trackNbr]

    def getSpecificTrack(self, trackNbr: int):
        """ Returns a specific track at trackNbr """

        if trackNbr >= self.numberOfTracks or trackNbr < 0:
            # Return None if trackNbr is not within bounds
            return None

        return self.file.tracks[trackNbr]

    def loopTrack(self, trackNbr: int, numLoops: int):
        """ Loops the melody at trackNbr, numLoops times"""

        if trackNbr >= self.numberOfTracks or trackNbr < 0 or numLoops < 1:
            # Do nothing if the trackNbr is not within bounds
            return

        self.subMelodies[trackNbr].loop(numLoops)
        self.rebuildMelodyTrack(trackNbr)

    def duplicateTrack(self, srcNbr, destNbr):
        """ Copies the melody of the track at srcNbr to track destNbr """

        if (max(srcNbr, destNbr) >= self.numberOfTracks
                or min(srcNbr, destNbr) < 0):
            # If one of the indices is not within bounds, do nothing
            return

        newMelody = self.subMelodies[srcNbr].duplicate()
        self.addMelody(destNbr, newMelody)

    def addTrack(self, name=""):
        """ Appends an empty track to the melody stack """

        self.numberOfTracks += 1
        self.subMelodies.append(Melody([], bpm=self.bpm, scale=self.scale,
                                       time_sig=self.time_sig,
                                       key_sig=self.key_sig))
        self.file.tracks.append(MidiTrack())

        if name == "":
            self.file.tracks[-1].name = "Track {}".format(
                self.numberOfTracks - 1
            )
        else:
            self.file.tracks[-1].name = name

    def deleteTrack(self, trackNbr):
        """ Deletes the track at index trackNbr"""

        if 0 > trackNbr > self.numberOfTracks - 1:
            # Do nothing if the trackNbr is not within bounds
            return

        x = self.subMelodies.pop(trackNbr)
        if len(x) > 0:
            self.tracksFilled -= 1

        self.file.tracks.pop(trackNbr)
        self.numberOfTracks -= 1

    def renameTrack(self, trackNbr, newName):
        """ Renames the track at index trackNbr to be called name """

        if 0 > trackNbr > self.numberOfTracks - 1:
            # Do nothing if the trackNbr is not within bounds
            return

        self.file.tracks[trackNbr].name = newName
