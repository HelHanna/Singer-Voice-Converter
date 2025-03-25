import os
import shutil

"""
This script was used to filter lab files corresponding to wav files
(ignoring txt files) as they were saved in separate folders
(could also be done manually by just copying all .lab and .wav files
and saving them separately, but for convinence you can use this script)
"""


main_folder = "Path/to/wavs"       
sub_folder = os.path.join(main_folder, "labels")  # LabelMakr saves the lab files in a subfolder called labels
destination_folder = "Destination/folder"    

# create a destination folder
os.makedirs(destination_folder, exist_ok=True)

# go through all wav files
for file in os.listdir(main_folder):
    if file.endswith(".wav"):
        wav_name = os.path.splitext(file)[0]  # Name without ending
        lab_file = f"{wav_name}.lab"  # lab name
        
        lab_path = os.path.join(sub_folder, lab_file)  # path to .lab file
        wav_path = os.path.join(main_folder, file)  # path to .wav file
        destination_wav_path = os.path.join(destination_folder, file)  
        destination_lab_path = os.path.join(destination_folder, lab_file) 

        # if suitable .lab file exists, copy both
        if os.path.exists(lab_path):
            shutil.copy(wav_path, destination_wav_path)
            shutil.copy(lab_path, destination_lab_path)
            print(f"copied: {file} + {lab_file} -> {destination_folder}")
        else:
            print(f"no corresponding lab file found for {file}.")

print("Done.")
