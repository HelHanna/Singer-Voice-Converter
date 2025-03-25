import os
import librosa
import numpy as np
import soundfile as sf

"""
This script classifies songs as being either more similar to song 1 or song 2.

Note: this script was used late in the classification process, 
when the sceams and rap parts were already extracted. Using this code in the
beginning would probably not lead to the desired results.

"""

# set the path to your audio folder
audio_folder = "Your/folder"
output_folder = os.path.join(audio_folder, "classified_songs")

# create folders for the output (the comparison)
song1_folder = os.path.join(output_folder, "song1_similar")
song2_folder = os.path.join(output_folder, "song2_similar")
os.makedirs(song1_folder, exist_ok=True)
os.makedirs(song2_folder, exist_ok=True)

# select reference songs
song1_path = "Your/Path/reference/010006003.wav"
song2_path = "Your/Path/reference/010004012.wav"

# extract audio features
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        rms = np.mean(librosa.feature.rms(y=y))

        return np.array([zcr, flatness, centroid, bandwidth, rms])
    
    except Exception as e:
        print(f"error in {file_path}: {e}")
        return None  

# load reference songs
features_song1 = extract_features(song1_path)
features_song2 = extract_features(song2_path)

if features_song1 is None or features_song2 is None:
    print("reference songs couln't be loaded!")
    exit()

# classify a song as being more similar to either of the reference songs
def classify_song(file_path):
    features = extract_features(file_path)
    if features is None:
        return None  
    
    # calculate distance
    dist1 = np.linalg.norm(features - features_song1)
    dist2 = np.linalg.norm(features - features_song2)

    return "song1_similar" if dist1 < dist2 else "song2_similar"

# go through all songs that you want to compare
for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)

    if filename.endswith(".wav"):  
        category = classify_song(file_path)
        if category:
            output_path = os.path.join(output_folder, category, filename)
            sf.write(output_path, *librosa.load(file_path, sr=None))  
            print(f"{filename} → {category}")

    elif filename.endswith(".txt"):  
        wav_path = file_path.replace(".txt", ".wav")
        if os.path.exists(wav_path):  
            category = classify_song(wav_path)
            if category:
                output_path = os.path.join(output_folder, category, filename)
                os.rename(file_path, output_path)
                print(f"{filename} (TXT) → {category}")

print("all wavs have been classified!")
