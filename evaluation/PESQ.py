import glob
import os
import sys

import librosa
import numpy as np
from pesq import pesq

ORIGINAL_PATH: str = sys.argv[1]
SYNTHESIZED_PATH: str = sys.argv[2]

wav_org: list[str] = glob.glob(ORIGINAL_PATH + "/*")
wav_org.sort()


def calculate_PESQ(path: str) -> None:
    """Calculate Perceptual Evaluation of Speed Quality value for sound files
    at `path`.

    Args:
        path (str): The path to calculate PESQ for

    Returns:
        score (float): The calculated PESQ value (MOS-LQO)
    """
    wav_synth: list[str] = glob.glob(path + "/*")
    wav_synth.sort()

    length: int = len(wav_org)
    score: list[float] = []
    for i in range(length):
        try:
            wo: np.ndarray
            ws: np.ndarray
            _: int | float
            wo, _ = librosa.load(wav_org[i], sr=16000)
            ws, _ = librosa.load(wav_synth[i], sr=16000)
            n: int = len(wo) - len(ws)
            if n > 0:
                ws = np.hstack((ws, np.zeros(abs(n))))
            elif n < 0:
                wo = np.hstack((wo, np.zeros(abs(n))))
            score.append(pesq(16000, wo, ws))
        except IndexError:
            # One of the original sound files was not synthesized
            print(f"Ignoring missing synthesized file {wav_org[i]}")

    # Print the PESQ value for the current folder
    print(f"PESQ ({path}): {np.mean(score)}")


if __name__ == "__main__":
    for item in os.listdir(SYNTHESIZED_PATH):
        # Ignore regular files in SYNTHESIZED_PATH
        if os.path.isfile(os.path.join(SYNTHESIZED_PATH, item)):
            continue

        # Ignore folder containing the original sound files
        if os.path.abspath(
            os.path.join(SYNTHESIZED_PATH, item)
        ) == os.path.abspath(ORIGINAL_PATH):
            continue

        # Calculate PESQ value for folder in SYNTHESIZED_PATH
        calculate_PESQ(os.path.join(SYNTHESIZED_PATH, item))
