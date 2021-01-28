def limiter(val):
    """ Caps val so that highest return value is 127 and lowest is 0 """
    if val > 127:
        return 127
    elif val < 0:
        return 0

    return val

class Note:
    def __init__(self, nbr, length, vel=64):
        self.nbr = nbr  # MIDI Number for Note
        self.length = length  # Length of Note (How Long it is Pressed)
        self.vel = vel  # Velocity (0 for Rest)

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

    def getMidiNumber(self):
        return self.nbr

    def getLength(self):
        return self.length

    def getVelocity(self):
        return self.vel

    def getOctave(self):
        return (self.nbr // 12) - 1

    def getName(self):
        """ Returns the name of the musical note this note corresponds to """
        if self.vel == 0:
            return "Rest"

        order = self.nbr % 12  # Position in octave (Ex: 0 - C, 1 - C#,...)
        return ['C', 'C#', 'D', 'D#',
                'E', 'F', 'F#', 'G',
                'G#', 'A', 'A#', 'B'][order]

    def getLengthTime(self, timeRes):
        """ Returns length of a note in units of time (for MIDI message) """
        return self.length * (timeRes // 8)

    def setMidiNumber(self, new_nbr):
        self.nbr = limiter(new_nbr)

    def setLength(self, new_length):
        self.length = new_length

    def setVelocity(self, new_vel):
        self.vel = limiter(new_vel)

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