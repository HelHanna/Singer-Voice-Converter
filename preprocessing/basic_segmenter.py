#script to automatic segment a .wav file based on silences; silence length and decibel threshold can be adjusted

from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

# Function to segment audio into song phrases based on silence
def segment_audio(input_file, start, file_name, output_folder='presegmented_data'):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Segment the audio based on silence
    segments = split_on_silence(
        audio,
        min_silence_len=5000,  # Minimum silence length
        silence_thresh=-40,    # decibel threshold
    )

    for i, segment in enumerate(segments):
        segment_number = start + i 
        segment_file = os.path.join(output_folder, file_name + f"{segment_number:03}.wav")
        segment.export(segment_file, format="wav")

file_name = str(input("give the filename: "))  # Path to  .wav file
input_file = "data/" + file_name + ".wav"
start = 0  # Change this value to start numbering from a specific number
segment_audio(input_file, start, file_name)
