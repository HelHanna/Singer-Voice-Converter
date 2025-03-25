import whisper_timestamped as whisper
import subprocess
import os

"""
This script uses whisper_timestamped in order to generate small segments together
with their corresponding text. 
Complete songs will be cut into small pieces and their corresponding text will be saved 
as a txt file with the same name.
The script was altered a couple of times to achieve the best possible result. 
We increased the required segment length to at least four seconds and tried to avoid hard cuts
to make the next steps (the labelling) as good as possible
"""

# we load the model (surprisingly small gave better results than the larger ones)
# small.en improved the text extraction further
model = whisper.load_model("small.en")

base_folder = "Your/Songs"

# go through all files
for root, _, files in os.walk(base_folder):
    for filename in files:
        if filename.endswith(".wav") or filename.endswith(".mp3"):  
            audio_path = os.path.join(root, filename)
            
            # keep the first numbers of the file name
            base_name = os.path.splitext(filename)[0]  # remove ending 
            
            # here 3 digits, adjust according to your needs
            if not base_name[:3].isdigit():
                print(f"warning: {filename} has no enumeration! skipping file.")
                continue

            print(f"processing file: {filename} ({base_name})")

            # transcribe audio file with time stemps
            result = whisper.transcribe(model, audio_path)
            segments = result["segments"]
            total_segments = len(segments)

            # Iterate over recognized segments
            i = 0
            segment_counter = 1
            while i < total_segments:
                start = segments[i]["start"]
                end = segments[i]["end"]

                # save text of combined segments
                combined_text = segments[i]["text"]

                # wavs must be at least 4 seconds long for postprocessing
                j = i + 1
                while j < total_segments and (segments[j]["start"] - start) < 4:
                    end = segments[j]["end"]
                    combined_text += " " + segments[j]["text"]  
                    j += 1

                
                if j < total_segments:
                    end = segments[j]["start"] - 0.1  # avoid hard cuts

                # ensure that a segment is at least 4 seconds long
                if end - start < 4:
                    print(f"skipping segment {segment_counter}, as it is too short ({end-start:.2f}s).")
                    i = j  
                    continue

                # generate segment numbers (001, 002, 003 …)
                segment_number = f"{segment_counter:03d}"
                final_name = f"{base_name}{segment_number}"  

                # define the paths for saving your segments
                segment_audio_path = os.path.join(root, f"{final_name}.wav")
                segment_text_path = os.path.join(root, f"{final_name}.txt")

                print(f"Segment {final_name}: {start:.2f}s - {end:.2f}s : {combined_text}")

                # save text in txt files
                with open(segment_text_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(combined_text)

                # ensure end > start before saving a segment
                if end > start:
                    command = f'ffmpeg -i "{audio_path}" -ss {start} -to {end} -c copy "{segment_audio_path}" -y'
                    subprocess.run(command, shell=True, check=True)
                else:
                    print(f"Skipping segment {final_name}, as end time ({end:.2f}s) smaller than starting time ({start:.2f}s).")

                segment_counter += 1
                i = j  # jump to the next unused segment

            print(f"segments of {filename} saved in {root}.\n")

print("All audios processed successfully.")