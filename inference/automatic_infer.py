#script for automatic inference of all .ds files in several folders

import os
import subprocess

def inference(experiment_name, output_name):
    folder_path = "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/evaluation/variance_ds"
    experiment_name = experiment_name
    output_path = "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/evaluation/" + output_name

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ds"):  # Check if the file has a .ds extension
            file_path = os.path.join(folder_path, file_name)
            command = ["python", "/nethome/hjhoppe/softwareprojekt/code/DiffSinger/scripts/infer.py", "acoustic", "--out", output_path, "--exp", experiment_name,  file_path]
            
            print(f"Running command: {' '.join(command)}")
            subprocess.run(command, check=True)

experiments = [("acoustic_chester_v5_3", "v5_3")] #example folders
for experiment, output in experiments:
    inference(experiment, output)