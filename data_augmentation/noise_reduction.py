import os
import librosa
import soundfile as sf
import re
import shutil
import numpy as np
import scipy.signal
import noisereduce as nr

"""
This script is part of the data augmentation. 
It slightly denoises the wav files

"""

input_folder = "Path/to/wavs"
output_folder = "Output/Path"
txt_eingabe_ordner = "Path/to/txts"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".wav") and re.search(r'\b\d{9}\b', filename):
        filepath = os.path.join(input_folder, filename)
        y, sr = librosa.load(filepath, sr=44100)

        # High-pass filter: set to 50 Hz (not that strict)
        b, a = scipy.signal.butter(6, 50 / (sr / 2), btype='highpass')
        y_filtered = scipy.signal.filtfilt(b, a, y)

        # Noise Reduction: reduce noise to 30% (again not to strict)
        y_denoised = nr.reduce_noise(y=y_filtered, sr=sr, prop_decrease=0.3)

        sf.write(os.path.join(output_folder, f"denoised_{filename}"), y_denoised, sr)

print("noise reduction done!")

# save txts denoised_
for dateiname in os.listdir(txt_eingabe_ordner):
    if dateiname.endswith(".txt") and re.search(r'\b\d{9}\b', dateiname):
        txt_pfad = os.path.join(txt_eingabe_ordner, dateiname)
        neues_txt_name = f"denoised_{dateiname}"
        shutil.copy(txt_pfad, os.path.join(output_folder, neues_txt_name))

print("txts saved!")
