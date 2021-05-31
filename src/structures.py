import random
import numpy as np
from general import *

# About this file:
# This file contains functions that given the number of bars (numBars) of
# a melody and the number of notes in the melody (numNotes), returns an
# array of integers representing the length of each note in units of
# SMALLEST_NOTE (structure[0] = 8 means that the first note of the melody
# has the length of 8). If an error occurs in any of the functions, a
# empty array ([]) is returned.
# BIG NOTE: Most (if not all) things in here only work with 4/4 time sig

# Support Functions
def getLargestReasonableLength(totalSpace: int, numNotes: int):
    """ Given the number of SMALLEST_NOTE notes that can fit in the melody
        and the number of notes 'numNotes' in the melody, return a reasonable
        maximum note length based on preventing large intervals between note
        lengths (e.g. prevent 1 whole to be accompanied by 32 1/32th notes) """

    if numNotes == 1:  # If one note left, just return the entire space
        return totalSpace

    beatLengths = [SIXTEENTH_NOTE, DOTTED_SIXTEENTH_NOTE, EIGHTH_NOTE,
                   DOTTED_EIGHTH_NOTE, QUARTER_NOTE, DOTTED_QUARTER_NOTE,
                   HALF_NOTE, DOTTED_HALF_NOTE, WHOLE_NOTE, DOTTED_WHOLE_NOTE]
    i = len(beatLengths) - 1

    while i > 0:
        largeNote = beatLengths[i]
        if largeNote < totalSpace:  # If the note fits into the space
            # Check to see what happens if we did add the note to melody
            notes = numNotes - 1
            roomLeft = totalSpace - largeNote
            if notes == 0:
                if roomLeft < 0:  # Adding note takes us over space limit
                    beatLengths.pop()
                    i -= 1
                else:
                    break
            else:
                # For the leftover notes
                equalLength = roomLeft // notes

                if equalLength < EIGHTH_NOTE:
                    # If we keep large note, every other note will be less
                    # than an eighth note long. Use a different large note
                    beatLengths.pop()
                    i -= 1
                else:
                    break
        else:  # Move on to next largest note
            beatLengths.pop()
            i -= 1

    if len(beatLengths) > 0:  # If we found a reasonable large note
        return beatLengths[-1]

    return THIRTY_SECOND_NOTE

def chooseRandomLength(lengths: List[int], normalDist: bool = True):
    """ Given an array of possible lengths, return one of the lengths
        randomly picked by random library. If normalDist is true, the
        lengths in the array are given weights based on normal
        distribution (mean has highest probability of getting chosen
        and probability gets smaller the farther you get away from mean """

    if len(lengths) > 1:
        if not normalDist:
            return random.choice(lengths)

        # Make an array that would represent a normal distribution
        xAxis = np.linspace(lengths[0], lengths[-1],
                            len(lengths))
        mean = np.mean(xAxis)
        stDev = np.std(xAxis)
        probDensity = ((np.pi * stDev) *
                       np.exp(-0.5 * ((xAxis - mean) / stDev) ** 2))

        weights = list(map(int, list(probDensity)))
        weights = list(map(lambda x: x + 1, weights))

        # Choose random note length with more probability towards the
        # mean and less probability of choosing the ends of the
        # possibleLengths array
        results = random.choices(lengths, weights, k=1)
        return results[0]
    else:
        if lengths:
            return lengths[0]

        return THIRTY_SECOND_NOTE

def closestToBeat(length: int):
    """ Returns the largest defined beat length less than parameter length """

    if length == 1:
        return 1

    possibleLengths = [SIXTEENTH_NOTE,
                       DOTTED_SIXTEENTH_NOTE, EIGHTH_NOTE, DOTTED_EIGHTH_NOTE,
                       QUARTER_NOTE, DOTTED_QUARTER_NOTE, HALF_NOTE,
                       DOTTED_HALF_NOTE, WHOLE_NOTE, DOTTED_WHOLE_NOTE]

    i = len(possibleLengths) - 1
    while i >= 0:
        if possibleLengths[i] <= length:
            return possibleLengths[i]

        i -= 1

    return 1  # If function works correctly, this line should never execute

def availableBeats(upperLimit: int, lowerLimit: int = -1):
    """ Given an upper limit, returns an array of beat lengths where the
        max is less than or equal to upper limit. If lowerLimit is -1,
        no lowerLimit is observed. Else, the min of the array is greater
        than or equal to lower limit """

    if upperLimit == 1:
        return []

    temp = [SIXTEENTH_NOTE, DOTTED_SIXTEENTH_NOTE, EIGHTH_NOTE,
            DOTTED_EIGHTH_NOTE, QUARTER_NOTE, DOTTED_QUARTER_NOTE, HALF_NOTE,
            DOTTED_HALF_NOTE, WHOLE_NOTE, DOTTED_WHOLE_NOTE]

    i = len(temp) - 1
    while temp[i] > upperLimit:
        temp.pop()
        i -= 1

        if i <= -1:
            break

    if lowerLimit > 2:
        while temp[0] < lowerLimit:
            temp.pop(0)

            if len(temp) == 0:
                break

    if temp:
        return temp

    return []  # This line should never execute


# Structure Functions
def getRandomStructure(numBars: int, numNotes: int, lengthFilter: bool = True):
    """ Returns a random array of note lengths. If lengthFilter is True, then
        the lengths of the notes will have a specified range that they appear
        between based on the number of notes and bars in the melody. If False,
        there is no limit/range """

    if numNotes > (numBars * SMALLEST_NOTE):
        return [], 0

    # Array of note lengths in units of SMALLEST_NOTE notes
    structure = []

    # Amount of notes of size SMALLEST_NOTE left to be filled in the melody
    roomLeft = numBars * SMALLEST_NOTE

    if lengthFilter:
        for n in range(numNotes):
            if n == numNotes - 1:
                # Range from a small note to the highest note length that
                # can fit in the space left
                possibleLengths = list(range(min(EIGHTH_NOTE, roomLeft),
                                             roomLeft + 1))
            else:
                # Create range where the equal length note is roughly in the
                # middle of the range and the max value is a reasonable one
                equalLength = roomLeft // (numNotes - n)
                largestNote = getLargestReasonableLength(roomLeft,
                                                         numNotes - n)
                deviation = largestNote - equalLength
                possibleLengths = list(range(max(1, equalLength - deviation),
                                             largestNote + 1))

            chosenLength = chooseRandomLength(possibleLengths)
            roomLeft -= chosenLength
            structure.append(chosenLength)
    else:
        # Every possible note length from 1 to dotted whole note
        possibleLengths = list(range(1, DOTTED_WHOLE_NOTE+1))

        for n in range(numNotes):
            while (len(possibleLengths) > 0 and
                   (roomLeft - (numNotes - n - 1)) < possibleLengths[-1]):
                # Condense possibleLengths array so that we only randomly
                # choose a length of a note that is possible to fit into melody
                # while leaving room for remaining notes
                possibleLengths.pop()

                if len(possibleLengths) == 0:
                    # Only a 1/32th note can fit
                    possibleLengths = [THIRTY_SECOND_NOTE]
                    break

            # Choose random note length out of possible lengths
            length = random.choice(possibleLengths)
            roomLeft -= length
            structure.append(length)

    return structure, roomLeft

def getEqualStructure(numBars: int, numNotes: int):
    """ Returns an array of note lengths where each length is (roughly) equal
        to the other note lengths """

    if numNotes > (numBars * SMALLEST_NOTE):
        # Physically cannot
        return [], 0

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

    return structure, 0

def getBeatStructure(numBars: int, numNotes: int, lengthFilter: bool = True):
    """ Returns a random array of note lengths where each length is a fraction
        or a multiple of a beat (NOTE: ONLY WORKS WITH 4/4 TIME SIG AS OF
        NOW) (e.g. quarter note, half note, eighth note, etc.). If
        lengthFilter is True, there is a specified range that the note lengths
        will be between. If False, there is no limit/range """

    structure = []

    possibleLengths = [SIXTEENTH_NOTE, DOTTED_SIXTEENTH_NOTE, EIGHTH_NOTE,
                       DOTTED_EIGHTH_NOTE, QUARTER_NOTE, DOTTED_QUARTER_NOTE,
                       HALF_NOTE, DOTTED_HALF_NOTE, WHOLE_NOTE,
                       DOTTED_WHOLE_NOTE]
    roomLeft = numBars * SMALLEST_NOTE

    if lengthFilter:
        for n in range(numNotes):
            if n == numNotes - 1:
                possibleLengths = availableBeats(roomLeft)
            else:
                # Create range where the equal length note is roughly in the
                # middle of the range and the max value is a reasonable one
                equalLength = roomLeft // (numNotes - n)
                largestNote = getLargestReasonableLength(roomLeft,
                                                         numNotes - n)
                deviation = largestNote - equalLength
                lowerLimit = closestToBeat(max(equalLength - deviation, 2))
                upperLimit = closestToBeat(largestNote)

                possibleLengths = availableBeats(upperLimit, lowerLimit)

            length = chooseRandomLength(possibleLengths)
            roomLeft -= length
            structure.append(length)
    else:
        for n in range(numNotes):
            while (len(possibleLengths) > 0 and
                   (roomLeft - (numNotes - n - 1)) < possibleLengths[-1]):
                # Condense possibleLengths array so that we only randomly
                # choose a length that is possible to fit into melody
                # while leaving room for remaining notes
                possibleLengths.pop()

            if len(possibleLengths) == 0:
                length = THIRTY_SECOND_NOTE
            else:
                length = random.choice(possibleLengths)

            roomLeft -= length
            structure.append(length)

    return structure, roomLeft

def getApprovedStructure(numBars: int, numNotes: int):
###############################  BACKLOG  #####################################
    """ Returns an array of note lengths where the returned structure
        represents a random compilation of smaller note structures that are
        popularly used in music (e.g. 1 bar with 1 note per beat + 1 bar
        with 1 note every off beat) """
    structure = []
    return structure

def getGuidedStructure(numBars: int, numNotes: int):
###############################  BACKLOG  #####################################
    """ Returns an array of note lengths where adjacent note lengths are
        dependent on each other based on the lengthRatings object.
        (e.g. A half note likes to come after another half note but a
              sixteenth note does not) """

    structure = []
    return structure