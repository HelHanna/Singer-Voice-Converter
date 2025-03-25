import librosa
import numpy as np

"""
This script compares the features of two audios.
It was also used to get an idea of which features 
are important to consider for the classification.

"""

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        # Compute spectral features
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        rms = np.mean(librosa.feature.rms(y=y))

        # Compute F0 variance (fundamental frequency variability)
        f0 = librosa.yin(y, fmin=80, fmax=1000)
        f0_filtered = f0[f0 > 0]  
        f0_var = np.var(f0_filtered) if len(f0_filtered) > 0 else 0

        # Compute syllable rate using onset detection
        onsets = librosa.onset.onset_detect(y=y, sr=sr)
        num_syllables = len(onsets)
        duration = librosa.get_duration(y=y, sr=sr)
        syllable_rate = num_syllables / duration if duration > 0 else 0

        return {
            "Syllable Rate": syllable_rate,
            "Bandwidth": spectral_bandwidth,
            "F0 Variance": f0_var,
            "Spectral Centroid": spectral_centroid,
            "RMS": rms
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def compare_audio(file1, file2):
    features1 = extract_features(file1)
    features2 = extract_features(file2)

    if features1 and features2:
        print("\nComparison of Audio Files \n")
        print(f"{'Feature':<20}{'File 1':<15}{'File 2':<15}{'Difference'}")
        print("="*60)

        for key in features1.keys():
            value1 = features1[key]
            value2 = features2[key]
            difference = value1 - value2
            print(f"{key:<20}{value1:.2f}{' ' * (15 - len(str(value1)))}{value2:.2f}{' ' * (15 - len(str(value2)))}{difference:.2f}")

# Example usage
file1 = "Your/Path/multi_voice_examples/001004004.wav"
file2 = "Your/Path/clear_examples/012016007.wav"

compare_audio(file1, file2)
