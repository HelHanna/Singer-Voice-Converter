import os
import numpy as np
import librosa
import shutil

"""
This script classifies songs as either screaming or singing as the screaming parts 
seemed to distort our initial model making the outputs quite noisy.
The classification is made by using F0. While there will still be some rough parts 
in the singing folder, the heavy screams and audience noise will be filtered out
"""

# select the folder containing the wav files
audio_folder = "Your/Path"

# make two directories for classifying the songs as either screaming or singing
clear_voice_folder = os.path.join(audio_folder, "clear_voice")
screaming_folder = os.path.join(audio_folder, "screaming")
os.makedirs(clear_voice_folder, exist_ok=True)
os.makedirs(screaming_folder, exist_ok=True)

# set the classification threshold based on the feature analysis (see: visualize_differences.py)
F0_MEAN_THRESHOLD = 230

# extract audio features
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        # calculate relevant features
        f0 = librosa.yin(y, fmin=80, fmax=1000)
        f0_filtered = f0[f0 > 0]  
        f0_mean = np.mean(f0_filtered) if len(f0_filtered) > 0 else 0

        return f0_mean
    except Exception as e:
        print(f"error in {file_path}: {e}")
        return None, None

# classify the wav files based on F0
def classify_audio(file_path):
    f0_mean = extract_features(file_path)

    if f0_mean is not None:
        if f0_mean > F0_MEAN_THRESHOLD:
            category = "screaming_noise"
            target_folder = screaming_folder
            reason = f"F0 Mean ({f0_mean:.2f}) > 225"
        else:
            category = "clear_voice"
            target_folder = clear_voice_folder
            reason = f"F0 Mean ({f0_mean:.2f}) ≤ 225"

        print(f"{os.path.basename(file_path)} → {reason}")
        return category, target_folder, reason

    return None, None, None

# move wav and txt files into their corresponding folder
def move_files(wav_path, target_folder, reason):
    filename = os.path.basename(wav_path)
    txt_filename = filename.replace(".wav", ".txt")

    txt_path = os.path.join(audio_folder, txt_filename)
    wav_target = os.path.join(target_folder, filename)
    txt_target = os.path.join(target_folder, txt_filename)

    shutil.move(wav_path, wav_target)
    print(f"moved {filename} → {target_folder} [{reason}]")

    if os.path.exists(txt_path):
        shutil.move(txt_path, txt_target)
        print(f"moved {txt_filename} → {target_folder}")

# go through all wav files in the main folder
for filename in os.listdir(audio_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_folder, filename)

        category, target_folder, reason = classify_audio(file_path)

        if category:
            move_files(file_path, target_folder, reason)

print("Everything is classified!")
