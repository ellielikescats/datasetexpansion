import music21
import pretty_midi as pm
import numpy as np

# Load the midi file
# midi_data = music21.converter.parse('/Users/eleanorrow/PycharmProjects/Leadsheet_dataset/lead-sheet-dataset/datasets/data/z/zabutom/zeta-force---blast-off-into-space/intro_key.mid')
midi_data = music21.converter.parse('/Users/eleanorrow/PycharmProjects/datasetexpansion/data/z/zhu/cocaine-model/verse_key.mid')
#midi_data = pm.PrettyMIDI('/Users/eleanorrow/PycharmProjects/Leadsheet_dataset/lead-sheet-dataset/datasets/data/z/zabutom/zeta-force---blast-off-into-space/intro_nokey.mid')

# Get the melody and harmony parts
for part in midi_data.parts:
    instrument_name = part.getInstrument().instrumentName
    print(instrument_name)

first_part = midi_data.parts[0]
second_part = midi_data.parts[1]

'''Jazz harmony Functions for expanding chords'''

def add_fourth(root_note,chord): # use for minor triads
    fourth_note = root_note.transpose('P4')
    chord.add(fourth_note)
    print(f"Added a 4th note: {fourth_note.name} to the chord")
    return

def add_raised_fourth(root_note,chord): # use for minor triads, need to remove the fifth though
    raised_fourth_note = root_note.transpose('A4')
    chord.add(raised_fourth_note)
    chord.remove(chord.fifth) # does this work to remove the fifth?
    print(f"Added a raised 4th note: {raised_fourth_note.name} to the chord")
    return


def add_sixth(root_note,chord): # use for major and minor triads
    sixth_note = root_note.transpose('M6') # - need to check that this is correct transposition
    chord.add(sixth_note)
    print(f"Added a 6th note: {sixth_note.name} to the chord")
    return

def add_major_seventh(root_note,chord): # use for major triads
    s7th_note = root_note.transpose('M7')
    chord.add(s7th_note)
    print(f"Added a major 7th note: {s7th_note.name} to the chord")
    return

def add_minor_seventh(root_note,chord): # use for minor triads
    s7th_note = root_note.transpose('m7')
    chord.add(s7th_note)
    print(f"Added a minor 7th note: {s7th_note.name} to the chord")

def add_ninth(root_note,chord): # can be used for all chords
    n9th_note = root_note.transpose('M9')
    chord.add(n9th_note)
    print(f"Added a 9th: {n9th_note.name} to the chord")
    return

def add_eleventh(root_note,chord):
    el11th_note = root_note.transpose('P11')
    chord.add(el11th_note)
    print(f"Added an 11th: {el11th_note.name} to the chord")
    return
def add_thirteenth(root_note,chord): # used for dominant 7th chords
    th13th_note = root_note.transpose('M13') # - need to check that this is correct transposition (should be the same note as 6th)
    chord.add(th13th_note)
    print(f"Added a 13th: {th13th_note.name} to the chord")
    return

''' if it is a ii-V-I progression...
if it is a major ii-V-I progression:

if it is a minor ii-V-i progression:
the third note of that chord will be a minor 3rd
The ii chord has a flatted 5th (aka a “half-diminished” chord) and the V is an altered dominant.


'''

''' need to add:
- any cluster chords? So this would also be 9ths/11ths/7ths etc I guess
- potentially identify the ii-V-I progression and add to these chords'''


def chord_to_extended_chord(chord, key, tonic, subdominant, dominant):
    # Get the root and bass note
    root_note = chord.root()
    bass_note = chord.bass()
    print("Original root note:", root_note.name)
    print("Bass note:", bass_note.name)

    # If the root note is not the same as the bass note, update the root note
    if root_note.name != bass_note.name:
        root_note = bass_note
        print("Updated root note to:", root_note.name)

    # If the chord quality is not defined, add the root note an octave higher
    if chord.quality == 'other':
        # Add the root note an octave higher
        chord.add(root_note.transpose('P8'))

    # If the chord is a major triad and not the dominant, add the 7th (major 7th)
    if chord.isMajorTriad() and root_note.name != dominant.name: # eventually want to add some randomness - could use the random module
        add_major_seventh(root_note,chord)

    # If the chord is a major triad and the dominant, add the 7th (dominant 7th)
    if chord.isMajorTriad() and root_note.name == dominant.name:
        # Find the dominant 7th note
        dom7th_note = root_note.transpose('M7')
        # If the dominant 7th isn't diatonic, adjust it to fit the key
        if dom7th_note.name not in key.getScale().getPitches():
            if key.mode == 'major':
                dom7th_note = dom7th_note.transpose('-A1')  # lowering by a half step
            else:
                # Assuming harmonic minor for simplicity
                dom7th_note = dom7th_note.transpose('+A1')  # raising by a half step
        # Add the dominant 7th note to the chord
        chord.add(dom7th_note)
        print(f"Added the dominant 7th note: {dom7th_note.name} to the chord")

    # If the chord is a major triad, add the 7th

    return


'''Functions for expanding melody'''

# Inspect the first 5 notes of the first part
# print("First part notes:", [note.name for note in first_part.flat.notes[:5]])
# Inspect the first 5 chords of the second part

# Work out the key of the midi file
music_key = midi_data.analyze('key')
print(music_key)

# Work out basic main chords in the key
tonic = music_key.tonic
print("Tonic:", tonic.name)
subdominant = tonic.transpose('P4')
print("Subdominant:", subdominant.name)
dominant = tonic.transpose('P5')
print("Dominant:", dominant.name)

for chord in second_part.flat.getElementsByClass(music21.chord.Chord):
    # Print the chord's pitches and duration
    print(f"Chord pitches: {', '.join(str(pitch) for pitch in chord.pitches)} | Duration: {chord.duration.quarterLength} quarter notes")
    # Print the chord's root and quality
    print(f"Chord: {chord} | Quality: {chord.quality}")
    # Extend the chord to dominant 7th
    chord_to_extended_chord(chord, music_key, tonic, subdominant, dominant)



# Export the new MIDI file containing both parts
midi_data.write('midi', fp='test.mid')
