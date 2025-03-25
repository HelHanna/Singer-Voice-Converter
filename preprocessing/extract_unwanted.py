import os
import numpy as np
from pydub import AudioSegment
import shutil  # For moving files

"""
This script removes wavs with zero variance 
as they are silent and will cause an error in the labelling process

"""

audio_folder = "Your/folder"

# Define the folder for bad audio files
bad_folder = os.path.join(audio_folder, "bad_wavs")
os.makedirs(bad_folder, exist_ok=True)  # Create if it doesn't exist

# Define a threshold for minimum variance (adjust if needed)
VARIANCE_THRESHOLD = 1e-6  

# Function to check variance of an audio file
def has_low_variance(audio_path):
    try:
        audio = AudioSegment.from_wav(audio_path)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)

        # Normalize the samples (avoid extreme values affecting variance)
        samples = samples / np.max(np.abs(samples)) if np.max(np.abs(samples)) > 0 else samples

        # Calculate variance
        variance = np.var(samples)

        print(f"{os.path.basename(audio_path)} → Variance: {variance:.8f}")

        return variance < VARIANCE_THRESHOLD  # Returns True if variance is too low
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return True  # If an error occurs, assume the file is bad

# Scan and move low-variance WAVs & their corresponding TXT files
for filename in os.listdir(audio_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_folder, filename)
        bad_path = os.path.join(bad_folder, filename)

        txt_file = filename.replace(".wav", ".txt")  # Corresponding text file
        txt_path = os.path.join(audio_folder, txt_file)
        bad_txt_path = os.path.join(bad_folder, txt_file)

        if has_low_variance(file_path):
            print(f"Moving {filename} to {bad_folder}")
            shutil.move(file_path, bad_path)  # Move the WAV file

            if os.path.exists(txt_path):  # Check if the corresponding TXT file exists
                print(f"Moving {txt_file} to {bad_folder}")
                shutil.move(txt_path, bad_txt_path)  # Move the TXT file

print("✅ Low-variance files (WAV & TXT) have been moved to 'bad_wavs'.")
