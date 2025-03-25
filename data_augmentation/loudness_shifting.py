import os
import librosa
import soundfile as sf
import re
import shutil
import numpy as np

"""
This script is part of the data augmentation. 
It increases and decreases the loudness of the wav files
in order to make the model more robust to loudness variations

"""

input_folder = "Your/path/to/the/wav/files"
output_folder = "Your/path"
txt_eingabe_ordner = "Path/to/the/txt/files"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".wav") and re.search(r'\b\d{9}\b', filename):
        filepath = os.path.join(input_folder, filename)
        y, sr = librosa.load(filepath, sr=44100)

        # increase loudness by 10 %
        y_louder = y * 1.1
        sf.write(os.path.join(output_folder, f"louder_{filename}"), y_louder, sr)

        # decrease loudness by 10 %
        y_quieter = y * 0.9
        sf.write(os.path.join(output_folder, f"quieter_{filename}"), y_quieter, sr)

print("loudness variations done!")

# save two versions of txt files (louder and quieter --> needed for later processing)
for dateiname in os.listdir(txt_eingabe_ordner):
    if dateiname.endswith(".txt") and re.search(r'\b\d{9}\b', dateiname):
        txt_pfad = os.path.join(txt_eingabe_ordner, dateiname)
        
        for prefix in ["louder_", "quieter_"]:
            neues_txt_name = f"{prefix}{dateiname}"
            shutil.copy(txt_pfad, os.path.join(output_folder, neues_txt_name))

print("txt files saved!")
