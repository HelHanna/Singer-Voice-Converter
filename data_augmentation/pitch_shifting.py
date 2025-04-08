import os
import librosa
import soundfile as sf
import re
import shutil

"""
This script is part of the data augmentation. 
It increases and decreases the pitch of the wav files
in order to make the model more robust to pitch variations

"""

input_folder = "Path/to/wavs"
output_folder = "Output/Path"
txt_eingabe_ordner = "Path/to/txts"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".wav") and re.search(r'\b\d{9}\b', filename): # note: the number is used as our files start with 9 digits, can be changed/removed according to your needs
        filepath = os.path.join(input_folder, filename)
        y, sr = librosa.load(filepath, sr=44100)

        # shift pitch +1 half note
        y_up = librosa.effects.pitch_shift(y, sr=sr, n_steps=1)
        sf.write(os.path.join(output_folder, f"up_{filename}"), y_up, sr)

        # shift pitch -1 half note
        y_down = librosa.effects.pitch_shift(y, sr=sr, n_steps=-1)
        sf.write(os.path.join(output_folder, f"down_{filename}"), y_down, sr)

print("Pitch-Shifting done!")


# save two versions of txts (down and up)
for dateiname in os.listdir(txt_eingabe_ordner):
    if dateiname.endswith(".txt") and re.search(r'\b\d{9}\b', dateiname):
        txt_pfad = os.path.join(txt_eingabe_ordner, dateiname)
        
        for prefix in ["down_", "up_"]:
            neues_txt_name = f"{prefix}{dateiname}"
            shutil.copy(txt_pfad, os.path.join(output_folder, neues_txt_name))

print("txts saved!")