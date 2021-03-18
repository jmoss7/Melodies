import random
import melody

# Array of different note lengths where repeats indicate probability of
# note being chosen by random (quarter note has highest probability)
# (Note: This currently only contains regular notes (no dotted notes),
# but this can be changed in the future)
possibleNotes = ([melody.THIRTY_SECOND_NOTE] +  # 1% Chance for 1/32th Note
                ([melody.SIXTEENTH_NOTE] * 10) +  # 10% Chance for 1/16th Note
                ([melody.EIGHTH_NOTE] * 18) +  # 18% Chance for 1/8th Note
                ([melody.QUARTER_NOTE] * 37) +  # 37% Chance for 1/4th Note
                ([melody.HALF_NOTE] * 23) +  # 23% Chance for 1/2th Note
                ([melody.WHOLE_NOTE] * 11))  # 11% Chance for Whole Note

def getRandomStructure(numBars, numNotes):
    """ Returns a random array of integers of length 'numNotes' that spans over
        'numBars' worth of music. In other words, the length of the returned
        array is numNotes and the sum of the returned array is numBars *
        SMALLEST_NOTE (see melodies.py) """

    # NOTE: In the future, this function can be optimized so that if there
    # is a lot of notes and not so much bars, it will try to evenly space
    # music lengths out as opposed to being totally random (e.g. if you
    # have one measure but then 16 notes, there should be a better chance
    # for the music to produce 16 16th notes as opposed to one half
    # note and 15 32th notes

    if numNotes > (numBars * melody.SMALLEST_NOTE):
        "Should be error, but for now..."
        return []

    # Array of note lengths in units of SMALLEST_NOTE notes
    structure = []

    # Amount of notes of size SMALLEST_NOTE left to be filled in the melody
    roomLeft = numBars * melody.SMALLEST_NOTE

    # Copy of possibleNotes array to allow for mutation of array by for loop
    pn = possibleNotes.copy()

    for n in range(numNotes):
        if n == numNotes - 1:
            # For last note, just take rest of the melody's length up
            structure.append(roomLeft)
        else:
            while (roomLeft - (numNotes - n - 1)) < pn[-1]:
                # Condense possible notes array so that we only randomly choose
                # a length of a note that is possible to fit into melody
                # while leaving room for remaining notes
                pn.pop()

                if len(pn) == 0:
                    # In reality, this should return an error. But right now...
                    return []

            length = random.choice(pn)
            roomLeft -= length
            structure.append(length)

    return structure

def getEqualNoteStructure(numBars, numNotes):
    """ Returns an array of integers of length 'numNotes' where each integer
        is (roughly) equal length and the notes (when played) spans over
        'numBars' worth of music """

    if numNotes > (numBars * melody.SMALLEST_NOTE):
        "Should be error, but for now..."
        return []

    # Array of note lengths in units of SMALLEST_NOTE notes
    structure = []

    # Amount of notes of size SMALLEST_NOTE left to be filled in the melody
    roomLeft = numBars * melody.SMALLEST_NOTE

    # The length of each note so that each note is roughly the same length
    equalLen = (numBars * melody.SMALLEST_NOTE) // numNotes

    for n in range(numNotes):
        if n == (numNotes-1):
            structure.append(roomLeft)
        else:
            roomLeft -= equalLen
            structure.append(equalLen)

    return structure