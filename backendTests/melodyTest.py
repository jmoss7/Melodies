import unittest
import melody

class TestMelody(unittest.TestCase):

    def test_createMelody(self):
        """ Tests the creation of an empty Melody object with the default
            parameters """

        emptyMelody = melody.Melody([])

if __name__ == '__main__':
    unittest.main()
