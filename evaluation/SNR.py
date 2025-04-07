import glob
import math
import os
import sys

import librosa
import numpy as np

ORIGINAL_PATH: str = sys.argv[1]
SYNTHESIZED_PATH: str = sys.argv[2]

wav_org: list[str] = glob.glob(ORIGINAL_PATH + "/*")
wav_org.sort()


def calculate_SNR(path: str) -> None:
    """Calculate Speech-to-noise ratio for sound files at `path`.

    Args:
        path (str): The path to calculate SNR for

    Returns:
        ratio (float): The calculated SNR value
    """
    wav_synth: list[str] = glob.glob(path + "/*")
    wav_synth.sort()

    length: int = len(wav_org)
    snr: list[float] = []
    for i in range(length):
        try:
            wo: np.ndarray
            ws: np.ndarray
            _: int | float
            wo, _ = librosa.load(wav_org[i], sr=None)
            ws, _ = librosa.load(wav_synth[i], sr=None)
            rmse_clean: float = math.sqrt(np.mean(wo**2))
            rmse_synth: float = math.sqrt(np.mean(ws**2))
            snr.append(10 * np.log10(rmse_clean / rmse_synth))
        except IndexError:
            # One of the original sound files was not synthesized
            print(f"Ignoring missing synthesized file {wav_org[i]}")
    print(f"SNR ({path}): {np.mean(snr)}")


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

        # Calculate SNR value for folder in SYNTHESIZED_PATH
        calculate_SNR(os.path.join(SYNTHESIZED_PATH, item))
