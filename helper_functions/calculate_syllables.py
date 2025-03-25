import os
import numpy as np
import librosa

"""
This script calculates the syllable rate, 
such that we can compare rap (which we want to exclude as it's not Chesters voice)
and singing voice
"""

# Ordnerpfade anpassen
rap_folder = "D:/all_segmented_live_albums_new/rap_examples"  # Beispiel-Rap-Ordner
clear_voice_folder = "D:/all_segmented_live_albums_new/clear_examples"  # Beispiel-Gesang-Ordner

def calculate_syllable_rate(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        
        # we use the onsets to count the syllables
        onsets = librosa.onset.onset_detect(y=y, sr=sr)
        num_syllables = len(onsets)
        
        # calculate the duration of the audio
        duration = librosa.get_duration(y=y, sr=sr)
        
        # the syllable rate is the number of syllables devided by the duration
        syllable_rate = num_syllables / duration if duration > 0 else 0
        return syllable_rate

    except Exception as e:
        print(f"error in {file_path}: {e}")
        return None


def analyze_syllable_rate(folder):
    rates = []
    for filename in os.listdir(folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(folder, filename)
            rate = calculate_syllable_rate(file_path)
            if rate is not None:
                rates.append(rate)

    avg_rate = np.mean(rates) if rates else 0
    return avg_rate, rates

# we compare the average syllable rate of (manually identified) rap and singing
avg_rap_rate, rap_rates = analyze_syllable_rate(rap_folder)
avg_clear_voice_rate, clear_voice_rates = analyze_syllable_rate(clear_voice_folder)

# 
print(f"average syllable rate of rap: {avg_rap_rate:.2f} syllables per second")
print(f"average syllable rate of singing: {avg_clear_voice_rate:.2f} syllables per second")
