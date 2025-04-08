import glob
import os
import sys

import librosa
import numpy as np
import pyworld as pw

ORIGINAL_PATH: str = sys.argv[1]
SYNTHESIZED_PATH: str = sys.argv[2]

Org_paths: list[str] = glob.glob(ORIGINAL_PATH + "/*")
Org_paths.sort()

sampling_rate = 44100
frame_period = 5.0


def extract_f0(wavs, fs, frame_period=5.0) -> list[np.ndarray]:
    """Extract F0 values from each file in `wavs`.

    Args:
        wavs (list[np.ndarray]): The list of wavs to extract the F0 values from
        fs (float): The sampling rate used for the wav files
        frame_period (float): Period between consecutive frames in milliseconds

    Returns:
        f0s (list[np.ndarray]): The list of extracted F0 values
    """
    f0s: list[np.ndarray] = []

    for i in range(len(wavs)):
        wav: np.ndarray = wavs[i]
        wav = wav.astype(np.float64)

        f0: np.ndarray
        _: np.ndarray
        f0, _ = pw.harvest(  # type: ignore
            wav, fs, frame_period=frame_period, f0_floor=71.0, f0_ceil=800.0
        )
        f0s.append(f0)

    return f0s


def calculate_F0_RMSE(path: str) -> None:
    """Calculate F0 root mean square error for sound files at `path`.

    Args:
        path (str): The path to calculate F0 RMSE for

    Returns:
        f0_rmse (float): The calculated F0 root mean square error
    """
    wavs_org: list[np.ndarray] = []
    wavs_synth: list[np.ndarray] = []

    Synth_paths: list[str] = glob.glob(path + "/*")
    Synth_paths.sort()

    for i in range(len(Org_paths)):
        try:
            wo: np.ndarray
            ws: np.ndarray
            _: int | float
            ws, _ = librosa.load(Synth_paths[i], sr=None)
            wo, _ = librosa.load(Org_paths[i], sr=None)
            wavs_synth.append(wo)
            wavs_org.append(ws)
        except IndexError:
            # One of the original sound files was not synthesized
            print(f"Ignoring missing synthesized file {Org_paths[i]}")

    # Flatten arrays for comparison
    f0s_org: np.ndarray = np.concatenate(
        extract_f0(
            wavs=wavs_org,
            fs=sampling_rate,
            frame_period=frame_period,
        )
    )
    f0s_synth: np.ndarray = np.concatenate(
        extract_f0(
            wavs=wavs_synth,
            fs=sampling_rate,
            frame_period=frame_period,
        )
    )

    # Pad shorter file with zeros to match the length of the longer one
    if len(f0s_synth) > len(f0s_org):
        f0s_org = np.pad(
            f0s_org,
            (0, len(f0s_synth) - len(f0s_org)),
            mode="constant",
            constant_values=0,
        )
    elif len(f0s_org) > len(f0s_synth):
        f0s_synth = np.pad(
            f0s_synth,
            (0, len(f0s_org) - len(f0s_synth)),
            mode="constant",
            constant_values=0,
        )

    # Calculate F0 RMSE
    F0RMSE = round(np.sqrt(np.mean((f0s_org - f0s_synth) ** 2)), 3)

    # Print the F0 RMSE value for the current folder
    print(f"F0 RMSE ({path}): {F0RMSE}")

    with open("f0_rmse_results.txt", "a") as file:
        file.write(f"F0 RMSE ({path}): {F0RMSE}\n")


if __name__ == "__main__":
    # Remove old results file if it exists
    if os.path.isfile("f0_rmse_results.txt"):
        os.remove("f0_rmse_results.txt")

    # Reference value, F0 RMSE with identical files
    calculate_F0_RMSE(ORIGINAL_PATH)

    for item in os.listdir(SYNTHESIZED_PATH):
        # Ignore regular files in SYNTHESIZED_PATH
        if os.path.isfile(os.path.join(SYNTHESIZED_PATH, item)):
            continue

        # Ignore folder containing the original sound files
        if os.path.abspath(
            os.path.join(SYNTHESIZED_PATH, item)
        ) == os.path.abspath(ORIGINAL_PATH):
            continue

        # Calculate F0 RMSE for folder in SYNTHESIZED_PATH
        calculate_F0_RMSE(os.path.join(SYNTHESIZED_PATH, item))
