import os
import librosa
import soundfile as sf
import re
import shutil


input_folder = "D:/LabelMakr_v030/corpus/song2_similar"
output_folder = "D:/LabelMakr_v030/corpus/song2_similar/augmented_wavs"
txt_eingabe_ordner = "D:/LabelMakr_v030/corpus/song2_similar"

# os.makedirs(output_folder, exist_ok=True)

# for filename in os.listdir(input_folder):
#     if filename.endswith(".wav") and re.search(r'\b\d{9}\b', filename):
#         filepath = os.path.join(input_folder, filename)
#         y, sr = librosa.load(filepath, sr=44100)

#         # Pitch Shifting um +2 Halbtöne
#         y_up = librosa.effects.pitch_shift(y, sr=sr, n_steps=1)
#         sf.write(os.path.join(output_folder, f"up_{filename}"), y_up, sr)

#         # Pitch Shifting um -2 Halbtöne
#         y_down = librosa.effects.pitch_shift(y, sr=sr, n_steps=-1)
#         sf.write(os.path.join(output_folder, f"down_{filename}"), y_down, sr)

# print("Pitch-Shifting abgeschlossen!")


#Überprüfen, welche TXT-Dateien existieren und zwei Versionen speichern
for dateiname in os.listdir(txt_eingabe_ordner):
    if dateiname.endswith(".txt") and re.search(r'\b\d{9}\b', dateiname):
        txt_pfad = os.path.join(txt_eingabe_ordner, dateiname)
        
        for prefix in ["down_", "up_"]:
            neues_txt_name = f"{prefix}{dateiname}"
            shutil.copy(txt_pfad, os.path.join(output_folder, neues_txt_name))

print("TXT-Dateien mit slow_ und fast_ hinzugefügt!")