import os
import numpy as np
import librosa
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# folders that contain examples of two different categories
# change categories according to your desired comparison
example_folders = {
    "clear_voice": "Your/Path/clear_examples",
    "multi_voice": "Your/Path/multi_voice_examples"
}

# extract the audio features of the example wavs
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        # compute the features
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        hnr = np.mean(librosa.effects.harmonic(y)) / np.mean(librosa.effects.percussive(y))
        f0 = librosa.yin(y, fmin=80, fmax=1000)
        f0_mean = np.mean(f0[f0 > 0]) if len(f0[f0 > 0]) > 0 else 0
        f0_var = np.var(f0[f0 > 0]) if len(f0[f0 > 0]) > 0 else 0
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        rms = np.mean(librosa.feature.rms(y=y))

        return [zcr, spectral_flatness, hnr, f0_mean, f0_var, spectral_centroid, spectral_bandwidth, rms]
    except Exception as e:
        print(f"⚠ Fehler bei {file_path}: {e}")
        return None

# save the data
data = []
for category, folder in example_folders.items():
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            file_path = os.path.join(folder, file)
            features = extract_features(file_path)
            if features:
                data.append([category, file] + features)

# construct a dataframe
columns = ["Kategorie", "Datei", "ZCR", "Spectral Flatness", "HNR", "F0 Mean", "F0 Var", "Spectral Centroid", "Spectral Bandwidth", "RMS"]
df = pd.DataFrame(data, columns=columns)

# save the data as a csv file for further analysis
csv_path = "feature_analysis_2.csv"
df.to_csv(csv_path, index=False)
print(f"feature data saved as {csv_path}")

# visualize the data
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))

# make a boxplot for every category
for feature in columns[2:]:  
    plt.figure(figsize=(8, 4))
    sns.boxplot(x="category", y=feature, data=df)
    plt.title(f"Boxplot of {feature}")
    plt.show()

# make scatterplot
sns.pairplot(df, hue="category", vars=["ZCR", "Spectral Flatness", "Spectral Centroid", "RMS"])
plt.show()
