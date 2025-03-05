import whisper_timestamped as whisper
import subprocess
import os
from pydub import AudioSegment

# Lade das Modell (z.B. "small", "medium", "large")
model = whisper.load_model("small")

# Pfad zum Ordner mit den Audiodateien
audio_folder = "C:/Users/hanna/OneDrive - Universität des Saarlandes/Dokumente/Semester 9/Software Project/Audios"


# Gehe alle Dateien im Audio-Ordner durch
for filename in os.listdir(audio_folder):
    if filename.endswith(".wav") or filename.endswith(".mp3"):  # ggf. weitere Formate hinzufügen
        audio_path = os.path.join(audio_folder, filename)
        audio_name = os.path.splitext(filename)[0]  # Dateiname ohne Endung
        
        # Erstelle einen Ausgabeordner für die Segmente des aktuellen Audios
        output_folder = os.path.join(audio_folder, f"Segments_{audio_name}")
        os.makedirs(output_folder, exist_ok=True)

        print(f"Verarbeite Datei: {filename}")

        # Transkribiere die aktuelle Audiodatei mit Zeitstempeln
        result = whisper.transcribe(model, audio_path)

        # Iterate über erkannte Segmente
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"] + 1.5

            # Dateipfade für Audio- und Text-Segment
            segment_audio_path = os.path.join(output_folder, f"segment_{i}.wav")
            segment_text_path = os.path.join(output_folder, f"segment_{i}.txt")

            # Text auch in die Konsole schreiben
            print(f"Segment {i}: {start:.2f}s - {end:.2f}s : {segment['text']}")

            # Text in eine .txt Datei schreiben
            with open(segment_text_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(segment["text"])

            # Mit FFmpeg den entsprechenden Ausschnitt extrahieren
            command = f"ffmpeg -i \"{audio_path}\" -ss {start} -to {end} -c copy \"{segment_audio_path}\" -y"
            subprocess.run(command, shell=True, check=True)

        print(f"Segmente für {filename} wurden in {output_folder} gespeichert.\n")

print("Alle Audios wurden erfolgreich verarbeitet.")
