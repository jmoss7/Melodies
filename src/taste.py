import shutil

from datetime import date
from general import *
from melody import Melody


def makeNotesString(notes):
    """ Takes a list of strings representing notes and converts it into one
        string in the format used in the taste.mel file """

    s = ""

    if isinstance(notes, Melody):
        for n in notes.sequence:
            name = n.getName()[:2]
            if name == "Rest":
                name = "R"

            s += name
    else:
        for n in notes:
            s += n

    return s


def makeNotesList(notes):
    """ Takes a string or melody representing notes and converts it
        into a list of strings suitable for taste.mel """

    arr = []

    if isinstance(notes, Melody):
        for n in notes.sequence:
            name = n.getName()[:2]
            if name == "Re":
                name = "R"

            arr.append(name)
    else:
        for n in notes:
            if n == '#':
                try:
                    arr[-1] += n
                except:
                    print("Error: Malformed taste.mel file. Unable to save"
                          + " new melody to file.")
                    return None
            else:
                arr.append(n)

    return arr


def noteToIndex(firstNote: str, offset: int = 0):
    """ Takes a note as a string and returns the index that the note
        represents in self.firstNotes """

    return {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6,
            "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11, "R": 12}.get(
        firstNote) + offset


def isGreater(first: str, second: str):
    if first.isdigit() or first == "\n":
        return False

    return noteToIndex(first) > noteToIndex(second)


class Taste:
    def __init__(self, fp: TextIO, backupFreq: int = 20):
        """ The Taste object is used to interface Melodies with a user's
            taste.mel file. The taste.mel file contains melodies that a user
            has generated and the corresponding rating they gave to each
            melody. This object allows the program to read from and write to
            the file during runtime. """

        self.fp = fp  # File pointer

        # firstNotes contains the index that each note below starts at in file
        # 0: C, 1: C#, 2: D, 3: D#, 4: E, 5: F, 6: F#, 7: G, 8: G#, 9: A,
        # 10: A#, 11: B, 12: Rest
        self.firstNotes = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        # Key: The noteString (see below) of a stored melody
        # Value: The stored rating of that melody
        self.ratings = {}

        self.updateCount = 0  # Number of times taste.mel has been changed
        self.updateFreq = backupFreq  # How often to backup taste.mel
        self.isReference = False  # Whether or not user can getRating from file

        # self.exists tells program if taste.mel is available and verified
        if not fp:
            self.exists = False
        else:
            self.exists = self.verifyHeader()

        self.loadMemory()
        print(self.firstNotes)

    def loadMemory(self):
        """ Initializes the ratings and firstNotes attributes of the taste
            file """

        self.fp.seek(0, 0)
        temp = self.fp.readlines()
        if len(temp) > 21:  # If there are more than 20 lines of melodies
            self.isReference = True

        self.fp.seek(20, 0)
        pos = 20
        possibleNotes = {"C": True, "D": True, "E": True, "F": True, "G": True,
                         "A": True, "B": True, "R": True}
        firstNote = True
        firstNotePos = 0
        noteBank = []

        c = self.fp.read(1)

        while c != '':
            if possibleNotes.get(c, False):
                if firstNote:
                    firstNotePos = pos
                    firstNote = False

                noteBank.append(c)
                pos += 1
            elif c == '#':
                if noteBank[-1] == 'R':
                    self.exists = False
                    return

                noteBank[-1] += "#"
                pos += 1
            else:
                if not(c.isdigit()) or (c.isdigit() and firstNote):
                    self.backup()
                    self.exists = False
                    return

                rating = ""
                while c.isdigit():
                    rating += c
                    c = self.fp.read(1)
                    pos += 1

                if int(rating) < 1:
                    self.ratings[makeNotesString(noteBank)] = 1
                elif int(rating) > 10:
                    self.ratings[makeNotesString(noteBank)] = 10
                else:
                    self.ratings[makeNotesString(noteBank)] = int(rating)

                firstNote = True
                if self.firstNotes[noteToIndex(noteBank[0])] == -1:
                    self.firstNotes[noteToIndex(noteBank[0])] = firstNotePos

                noteBank.clear()
                pos += 1

            c = self.fp.read(1)

    def verifyHeader(self):
        """ Checks to make sure that the header of the taste.mel file is
            correct (and creates a header if taste.mel is empty) """
        self.fp.seek(0, 0)
        header = self.fp.read(19)
        if header == "Melodies Taste File":
            return True

        if len(header) == 0:
            self.fp.seek(0, 0)
            self.fp.write("Melodies Taste File\n")
            return True

        return False

    def updateFirstNotePositions(self, idx, stringLen, pos):
        if self.firstNotes[idx] == -1:
            self.firstNotes[idx] = pos

        for i in range(idx + 1, 13):
            if self.firstNotes[i] != -1:
                self.firstNotes[i] += stringLen

    def getRating(self, m: Melody):
        """ Takes a melody m and returns the rating of the melody based on
            its notes and what's in the taste.mel file. If the melody is not
            in taste.mel, this function returns a rating based on related
            melodies in taste.mel """

        if not self.isReference or not self.exists:
            return -1

        curRating = -1

        notesString = makeNotesString(m)
        if self.ratings.get(notesString, False):
            return self.ratings[notesString]

        pastRatingLength = 0

        while True:
            extraLength = 0
            extraNotes = ""
            while notesString != '':
                extraNotes += notesString[-1]
                notesString = notesString[:-1]
                extraLength += 1

                if self.ratings.get(notesString, False):
                    if curRating == -1:
                        curRating = self.ratings[notesString]
                    elif pastRatingLength != extraLength:
                        oldRating = curRating
                        newRating = self.ratings[notesString]
                        sumLength = pastRatingLength + extraLength
                        curRating = (((oldRating * pastRatingLength) //
                                      sumLength) + ((newRating *
                                                     len(notesString))
                                                    // sumLength))
                    else:
                        curRating = ((curRating + self.ratings[notesString])
                                     // 2)

                    pastRatingLength += len(notesString)
                    break

            if notesString:
                if len(extraNotes) >= 3:
                    # Rating might not be as good due to extra one or two notes
                    curRating = max(curRating - 1, 1)
                    break
                else:
                    notesString = extraNotes
            else:
                break

        return curRating

    def srSetup(self, firstNote: str):
        startIdx = noteToIndex(firstNote)
        offset = 0
        while self.firstNotes[startIdx - offset] == -1:
            offset += 1
            if startIdx - offset == -1:
                break

        if startIdx - offset == -1:
            pos = 20
        else:
            pos = self.firstNotes[startIdx - offset]

        self.fp.seek(pos, 0)

        return startIdx, pos

    def setRating(self, m: Melody, rating: int):
        """ Takes a melody and stores its rating into taste.mel (overwrites
            previous rating if melody was already in file) """

        if not self.exists:
            return

        noteBank = makeNotesList(m)
        stringLength = len("".join(noteBank)) + len(str(rating)) + len("\n")
        startIdx, pos = self.srSetup(noteBank[0])
        storedBank = self.fp.readlines()
        if not storedBank:
            storedBank = []
        startPos = pos
        done = False

        for i in range(len(storedBank)):
            noteIdx = 0
            storedCount = 0
            skip = False
            sbl = makeNotesList(storedBank[i])
            if sbl is None:
                return

            for j in range(len(sbl)):
                c = sbl[j]

                if c != noteBank[noteIdx]:
                    if isGreater(c, noteBank[noteIdx]) and not skip:
                        storedBank.insert(i, "".join(noteBank))
                        storedBank[i] += str(rating) + "\n"
                        self.updateFirstNotePositions(startIdx,
                                                      stringLength, pos)
                        done = True
                        break
                    else:
                        pos += len(c)
                        storedCount += 1
                        noteIdx += 1
                        if not(c.isdigit()) and c != "\n":
                            skip = True
                else:
                    pos += len(c)
                    storedCount += 1
                    noteIdx += 1

                if noteIdx == len(noteBank):
                    if not skip:
                        if sbl[j+1].isdigit():
                            sbl = sbl[:j+1] + [str(rating), "\n"]
                            storedBank[i] = "".join(sbl)
                        else:
                            storedBank.insert(i, "".join(noteBank))
                            storedBank[i] += str(rating) + "\n"
                            self.updateFirstNotePositions(startIdx,
                                                          stringLength, pos)
                        done = True

                    break

            if done:
                break

        if not done:
            self.updateFirstNotePositions(startIdx, stringLength, pos)
            storedBank.append("")
            for n in noteBank:
                storedBank[-1] += n
            storedBank[-1] += str(rating) + "\n"

        self.fp.seek(startPos, 0)
        for line in storedBank:  # Do it line by line to avoid one big write
            self.fp.write(line)

        self.ratings[makeNotesString(noteBank)] = rating
        self.incrementSaves()

    def incrementSaves(self):
        if self.updateCount == self.updateFreq:
            self.updateCount = 0
            self.backup()
        else:
            self.updateCount += 1

    def backup(self):
        if self.exists:
            try:
                shutil.copyfile("../support-files/opt/taste.mel",
                                "../support-files/opt/taste(backup "
                                + "{}).mel".format(date.today()))
            except:
                print("Unable to make backup")

    def close(self):
        if self.exists:
            try:
                self.fp.close()
            except:
                print("Unable to close file object")
