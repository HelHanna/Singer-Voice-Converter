# script to automatically infer all .ds files in a folder with the variance model to prepare them for the acoustic model (only important for model 6)

import os
import subprocess

folder_path = "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/evaluation/simple_ds"  # Change this example to actual folder path
experiment_name = "variance_chester_v5_2"  # Change this example to experiment name
output_path = "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/evaluation/variance_ds" #Change this example to desired output path

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".ds"):  # Check if the file has a .ds extension
        file_path = os.path.join(folder_path, file_name)
        command = ["python", "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/scripts/infer.py", "variance", "--out", output_path, "--exp", experiment_name,  file_path] # create command for inference
        
        subprocess.run(command, check=True)  # Execute the command
