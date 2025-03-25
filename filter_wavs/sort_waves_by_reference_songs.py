import os
import numpy as np
import librosa
import shutil

"""
This script shifts wavs to the most similar category. 
Each category contains at least 10 example wavs that are used for comparison.

Note: we did not use this categorization in the end as 
there were to many outliers in each category.
It is just included as an example of our experiments.

"""



# load folders for comparison; each folder containing a couple of reference songs
example_folders = {
    "clear_voice": "D:/all_segmented_live_albums_new/clear_examples",
    "screaming": "D:/all_segmented_live_albums_new/screaming_examples",
    "multi_voice": "D:/all_segmented_live_albums_new/multi_voice_examples",
    "rap": "D:/all_segmented_live_albums_new/rap_examples"
}

# set path to songs you want to classify
audio_folder = "D:/all_segmented_live_albums_new"

# target folders
target_folders = {
    "clear_voice": os.path.join(audio_folder, "clear_voice"),
    "screaming": os.path.join(audio_folder, "screaming"),
    "multi_voice": os.path.join(audio_folder, "multi_voice"),
    "rap": os.path.join(audio_folder, "rap")
}
for folder in target_folders.values():
    os.makedirs(folder, exist_ok=True)


def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        hnr = np.mean(librosa.effects.harmonic(y)) / np.mean(librosa.effects.percussive(y))

        f0 = librosa.yin(y, fmin=80, fmax=1000)
        f0_mean = np.mean(f0[f0 > 0])  
        f0_var = np.var(f0[f0 > 0])  

        return np.array([zcr, spectral_flatness, hnr, f0_mean, f0_var])
    except Exception as e:
        print(f"error in {file_path}: {e}")
        return None

# calculate the average features
def get_average_features(folder):
    feature_list = []
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            file_path = os.path.join(folder, file)
            features = extract_features(file_path)
            if features is not None:
                feature_list.append(features)
    
    if len(feature_list) > 0:
        return np.mean(feature_list, axis=0)  
    else:
        print(f"no valid data found in {folder}!")
        return None

# calculate average features for each category
example_features = {}
for category, folder in example_folders.items():
    features = get_average_features(folder)
    if features is not None:
        example_features[category] = features


if len(example_features) != len(example_folders):
    print("error, example features could not be calculated for all categories!")
    exit()


def classify_audio(file_path):
    features = extract_features(file_path)
    if features is None:
        return None, None, None

    # calculate the distances
    distances = {
        category: np.linalg.norm(features - avg_features)
        for category, avg_features in example_features.items()
    }

    # find the best match
    best_match = min(distances, key=distances.get)
    return best_match, target_folders[best_match], f"most similar to {best_match.replace('_', ' ').title()}"

# shift audio files
def move_files(wav_path, target_folder, reason):
    filename = os.path.basename(wav_path)
    txt_filename = filename.replace(".wav", ".txt")

    txt_path = os.path.join(audio_folder, txt_filename)
    wav_target = os.path.join(target_folder, filename)
    txt_target = os.path.join(target_folder, txt_filename)

    shutil.move(wav_path, wav_target)
    print(f"{filename} → {target_folder} [{reason}]")

    if os.path.exists(txt_path):
        shutil.move(txt_path, txt_target)
        print(f"{txt_filename} → {target_folder}")


for filename in os.listdir(audio_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_folder, filename)

        category, target_folder, reason = classify_audio(file_path)

        if category:
            move_files(file_path, target_folder, reason)

print("classification finished!")
