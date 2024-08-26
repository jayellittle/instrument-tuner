"""
main.py - Instrument Tuner : Show dominant frequency of the recorded sound

Jun. 26, 2023 by Woo Sung Jahng

"""
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import math


# Function to calculate the dominant frequency
def calculate_dom_freq(signal, sample_rate):
    # Compute the Fourier transform
    frequencies = np.fft.fftfreq(len(signal), 1 / sample_rate)
    spectrum = np.fft.fft(signal)
    
    # Find the index of the maximum amplitude in the spectrum
    max_index = np.argmax(np.abs(spectrum))
    
    # Retrieve the dominant frequency
    dominant_frequency = frequencies[max_index]
    
    return abs(dominant_frequency)


# Function to calculate the closest musical note
def calculate_closest_note(frequency):
    C4_frequency = 261.63  # Frequency of C4 note
    closest_note = round(12 * math.log2(frequency / C4_frequency)) + 60
    note_names = [
        "C", "C#/D♭", "D", "D#/E♭", "E", "F", "F#/G♭", "G", "G#/A♭", "A", "A#/B♭", "B"
    ]
    octave = (closest_note // 12) - 1
    note_name = note_names[closest_note % 12]
    return f"{note_name}{octave}"


# Recording Parameters
duration = 1         # Duration [sec]
sample_rate = 44100  # Sample rate [Hz]

# Start recording
print("Recording started...")
while (True):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()

    # Get the recorded audio data
    audio_data = recording.flatten()

    # Calculate the dominant frequency
    dominant_freq = calculate_dom_freq(audio_data, sample_rate)
    print("Dominant Frequency:", dominant_freq, "Hz")

    # Calculate the closest note
    closest_note = calculate_closest_note(dominant_freq)
    print("Closest Note:", closest_note)
