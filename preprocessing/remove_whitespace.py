import os
import re

"""
This script removed unnecessary white-space in the 
txt-files to avoid errors with LabelMakr

"""


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

folder_path = "Path/to/txts"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # Datei lesen
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Text bereinigen
        cleaned_content = clean_text(content)

        # Datei überschreiben
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(cleaned_content)

        print(f"cleaned: {filename}")

print("Done!")
