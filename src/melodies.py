from mido import Message, MidiFile, MidiTrack


def main():

    # Tutorial from https://mido.readthedocs.io/en/latest/midi_files.html
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # twinkle twinkle
    track.append(Message('program_change', program=12, time=0))
    track.append(Message('note_on', note=60, velocity=64, time=64))
    track.append(Message('note_off', note=60, velocity=127, time=127))
    track.append(Message('note_on', note=60, velocity=64, time=64))
    track.append(Message('note_off', note=60, velocity=127, time=127))
    track.append(Message('note_on', note=67, velocity=64, time=64))
    track.append(Message('note_off', note=67, velocity=127, time=127))
    track.append(Message('note_on', note=67, velocity=64, time=64))
    track.append(Message('note_off', note=67, velocity=127, time=127))
    track.append(Message('note_on', note=69, velocity=64, time=64))
    track.append(Message('note_off', note=69, velocity=127, time=127))
    track.append(Message('note_on', note=69, velocity=64, time=64))
    track.append(Message('note_off', note=69, velocity=127, time=127))
    track.append(Message('note_on', note=67, velocity=64, time=64))
    track.append(Message('note_off', note=67, velocity=127, time=127))
    track.append(Message('note_off', note=65, velocity=64, time=64))
    track.append(Message('note_off', note=65, velocity=127, time=127))
    track.append(Message('note_on', note=65, velocity=64, time=64))
    track.append(Message('note_off', note=65, velocity=127, time=127))
    track.append(Message('note_on', note=65, velocity=64, time=64))
    track.append(Message('note_off', note=65, velocity=127, time=127))
    track.append(Message('note_on', note=64, velocity=64, time=64))
    track.append(Message('note_off', note=64, velocity=127, time=127))
    track.append(Message('note_on', note=64, velocity=64, time=64))
    track.append(Message('note_off', note=64, velocity=127, time=127))
    track.append(Message('note_on', note=62, velocity=64, time=64))
    track.append(Message('note_off', note=62, velocity=127, time=127))
    track.append(Message('note_on', note=62, velocity=64, time=64))
    track.append(Message('note_off', note=62, velocity=127, time=127))
    track.append(Message('note_on', note=60, velocity=64, time=64))
    track.append(Message('note_off', note=60, velocity=127, time=127))

    mid.save('example_midi.mid')
    return 0


if __name__ == '__main__':
    main()
