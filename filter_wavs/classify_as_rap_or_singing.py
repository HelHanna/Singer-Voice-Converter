import os
import numpy as np
import librosa
import shutil

"""
This script classifies wavs as either rap or singing.
The division is based on the syllable rate. While there will be still some misclassifications,
the overall division helps in drastically reducing the parts sung by Mike

"""
# wavs folder
clear_voice_folder = "Your/Path"

# create new folders for the separation
singing_voice_folder = os.path.join(clear_voice_folder, "singing_voice")
rap_voice_folder = os.path.join(clear_voice_folder, "rap_voice")

for folder in [singing_voice_folder, rap_voice_folder]:
    os.makedirs(folder, exist_ok=True)

# set a syllable threshold to determine if it is singing or rap based on the analysis (see: calculate_syllables.py)
SYLLABLE_RATE_THRESHOLD = 6  

# extract features
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        # count syllables
        onsets = librosa.onset.onset_detect(y=y, sr=sr)
        num_syllables = len(onsets)
        duration = librosa.get_duration(y=y, sr=sr)
        syllable_rate = num_syllables / duration if duration > 0 else 0

        #return syllable_rate
        return syllable_rate

    except Exception as e:
        print(f"error in {file_path}: {e}")
        return None, None

# classify the audios
def classify_audio(file_path):
    syllable_rate = extract_features(file_path)

    if syllable_rate is not None:
        if syllable_rate >= SYLLABLE_RATE_THRESHOLD:
            category = "rap_voice"
            target_folder = rap_voice_folder
            reason = f"Syllable rate ({syllable_rate:.2f}) ≥ {SYLLABLE_RATE_THRESHOLD}"
        else:
            category = "singing_voice"
            target_folder = singing_voice_folder
            reason = f"Syllable rate ({syllable_rate:.2f}) < {SYLLABLE_RATE_THRESHOLD}"
        
        print(f"📊 {os.path.basename(file_path)} → {reason}")
        return category, target_folder, reason

    return None, None, None

# move the files according to their syllable rate
def move_files(wav_path, target_folder, reason):
    filename = os.path.basename(wav_path)
    txt_filename = filename.replace(".wav", ".txt")

    txt_path = os.path.join(clear_voice_folder, txt_filename)
    wav_target = os.path.join(target_folder, filename)
    txt_target = os.path.join(target_folder, txt_filename)

    shutil.move(wav_path, wav_target)
    print(f"moved {filename} → {target_folder} [{reason}]")

    if os.path.exists(txt_path):
        shutil.move(txt_path, txt_target)
        print(f"moved {txt_filename} → {target_folder}")

# go through all the wavs in the input folder
for filename in os.listdir(clear_voice_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(clear_voice_folder, filename)

        category, target_folder, reason = classify_audio(file_path)

        if category:
            move_files(file_path, target_folder, reason)

print("Everything separated!")
