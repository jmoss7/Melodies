from general import limiter, QUARTER_NOTE

class Note:
    # Dunder methods (__method__)
    def __init__(self, nbr: int, length: int, vel: int = 64):
        """ Constructs a Note object, which contains the characteristics
            of a note """

        self.nbr = nbr  # MIDI Number for Note
        self.length = length  # Length of Note (How Long it is Pressed)
        self.vel = vel  # Velocity (0 for Rest)

    def __len__(self):
        """ Returns the length of the note in units SMALLEST_NOTE """

        return self.length

    def __str__(self):
        return "{}{}, {}, {}".format(self.getName(), self.getOctave(),
                self.length, self.vel)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """ Checks if two notes are same pitch (not length or velocity) """

        if not other.isinstance(Note):
            return False

        return self.nbr and other.nbr

    # GET and SET functions
    def getMidiNumber(self):
        """ Returns the MIDI number of the note """

        return self.nbr

    def getVelocity(self):
        """ Returns the velocity of the note """

        return self.vel

    def getOctave(self):
        """ Returns the octave of the note """

        return (self.nbr // 12) - 1

    def getName(self):
        """ Returns the name of the musical note this note corresponds to """

        if self.vel == 0:
            return "Rest"

        order = self.nbr % 12  # Position in octave (Ex: 0 - C, 1 - C#,...)
        return ['C', 'C#', 'D', 'D#',
                'E', 'F', 'F#', 'G',
                'G#', 'A', 'A#', 'B'][order]

    def getLengthTime(self, timeRes: int):
        """ Returns length of a note in units of time (for MIDI message) """

        # Note: a return value of timeRes represents a quarter note
        return self.length * (timeRes // QUARTER_NOTE)

    def setMidiNumber(self, new_nbr):
        """ Sets the MIDI number of the note """

        self.nbr = limiter(new_nbr)

    def setLength(self, new_length):
        """ Sets the length of the note in units SMALLEST_NOTE """

        self.length = new_length

    def setVelocity(self, new_vel):
        """ Sets the velocity of the note """

        self.vel = limiter(new_vel)

    # Additional functions
    def incrementOctave(self, delta):
        """ Increases (+ delta) or decreases (- delta) the current note in
            increments of octaves (keeps same musical note) """

        if delta != 0:
            self.nbr = limiter(self.nbr + (delta * 12))

    def duplicate(self):
        """ Creates a new Note object with the exact same characteristics
            as this note """

        return Note(self.nbr, self.length, self.vel)

    def semitoneChange(self, delta):
        """ Increases (+ delta) or decreases (- delta) the current note in
            increments of half steps """

        self.nbr = limiter(self.nbr + delta)