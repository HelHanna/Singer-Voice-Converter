import os
import librosa

""" 
this script calculates the duration of all 
wav files in order to keep track on how much data 
is actually included and trained in our model in the end
"""

audio_folder = "My/wavs"

# calculate the total duration
total_duration = 0.0

for filename in os.listdir(audio_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_folder, filename)
        y, sr = librosa.load(file_path, sr=None)  
        duration = librosa.get_duration(y=y, sr=sr)  
        total_duration += duration
        
print(f"total duration: {total_duration:.2f} seconds")
print(f"equivalent to {total_duration / 60:.2f} minutes")
