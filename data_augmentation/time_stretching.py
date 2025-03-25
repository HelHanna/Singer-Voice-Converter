import os
import librosa
import soundfile as sf
import re
import shutil

"""
This script is part of the data augmentation. 
It increases and decreases the speed of the wav files
in order to make the model more robust to speed variations

"""

input_folder = "Path/to/wavs"
output_folder = "Output/Path"
txt_eingabe_ordner = "Path/to/txts"

# make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Time-Stretching factors
time_stretch_faktoren = {"slow": 0.9, "fast": 1.1}  # 10% slower and 10% faster

for dateiname in os.listdir(input_folder):
    if dateiname.endswith(".wav") and re.search(r'\b\d{9}\b', dateiname):
        dateipfad = os.path.join(input_folder, dateiname)
        y, sr = librosa.load(dateipfad, sr=44100)

        for label, faktor in time_stretch_faktoren.items():
            y_stretched = librosa.effects.time_stretch(y, rate=faktor)
            sf.write(os.path.join(output_folder, f"{label}_{dateiname}"), y_stretched, sr)

print("time-streching done!")

# save two versions of txt files (slow and fast)
for dateiname in os.listdir(txt_eingabe_ordner):
    if dateiname.endswith(".txt") and re.search(r'\b\d{9}\b', dateiname):
        txt_pfad = os.path.join(txt_eingabe_ordner, dateiname)
        
        for prefix in ["slow_", "fast_"]:
            neues_txt_name = f"{prefix}{dateiname}"
            shutil.copy(txt_pfad, os.path.join(output_folder, neues_txt_name))

print("txt files saved!")