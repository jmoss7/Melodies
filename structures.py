import random
from general import *

# Array of different note lengths where repeats indicate probability of
# note being chosen by random (quarter note has highest probability)
# (Note: This currently only contains regular notes (no dotted notes),
# but this can be changed in the future)

def getRandomStructure(numBars: int, numNotes: int):
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

    if numNotes > (numBars * SMALLEST_NOTE):
        "Should be error, but for now..."
        return []

    # Array of note lengths in units of SMALLEST_NOTE notes
    structure = []

    # Amount of notes of size SMALLEST_NOTE left to be filled in the melody
    roomLeft = numBars * SMALLEST_NOTE

    # Possible note lengths
    pn = [SIXTEENTH_NOTE, DOTTED_SIXTEENTH_NOTE, EIGHTH_NOTE,
          DOTTED_EIGHTH_NOTE, QUARTER_NOTE, DOTTED_QUARTER_NOTE, HALF_NOTE,
          DOTTED_HALF_NOTE, WHOLE_NOTE, DOTTED_WHOLE_NOTE]
    weights = [1, 5, 10, 7, 25, 20, 15, 5, 10, 2]

    for n in range(numNotes):
        while len(pn) > 0 and (roomLeft - (numNotes - n - 1)) < pn[-1]:
            # Condense possible notes array so that we only randomly choose
            # a length of a note that is possible to fit into melody
            # while leaving room for remaining notes
            pn.pop()
            weights.pop()

            if len(pn) == 0:
                # Only a 1/32th note can fit
                break

        if len(pn) > 0:
            length = random.choices(pn, weights=weights, k=1)
        else:
            length = [THIRTY_SECOND_NOTE]

        roomLeft -= length[0]
        structure.append(length[0])

    return structure, roomLeft

def getEqualNoteStructure(numBars: int, numNotes: int):
    """ Returns an array of integers of length 'numNotes' where each integer
        is (roughly) equal length and the notes (when played) spans over
        'numBars' worth of music """

    if numNotes > (numBars * SMALLEST_NOTE):
        "Should be error, but for now..."
        return []

    # Array of note lengths in units of SMALLEST_NOTE notes
    structure = []

    # Amount of notes of length ((bars * SMALLEST_NOTE) // numNotes) that
    # the structure will have
    floorNotes = numNotes - ((numBars * SMALLEST_NOTE) % numNotes)

    # The length of each note so that each note is roughly the same length
    equalLen = (numBars * SMALLEST_NOTE) // numNotes

    for i in range(numNotes):
        if i >= floorNotes:
            structure.append(equalLen + 1)
        else:
            structure.append(equalLen)

    return structure