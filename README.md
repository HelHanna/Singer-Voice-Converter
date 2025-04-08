# 🎙️ Singing Voice Synthesis with Chester Bennington's Voice


## Project Overview
This project aims to emulate Chester Bennington's vocal style using a fine-tuned DiffSinger model. The goal is to generate a new rendition of a track from *From Zero* with Chester's distinctive timbre, vocal fry, and expressive pitch dynamics.

- **Model:** Fine-tuned DiffSinger
- **Output:** Model-generated vocals mixed into an instrumental track using Reaper.

## Dataset Creation
We compiled a dataset to capture the range of Chester’s vocal characteristics:

- **Source:** 8 Linkin Park albums 
- **Method:** Curated from YouTube for high-quality audio, focusing on both studio and live recordings to capture diverse vocal traits.

## Preprocessing Pipeline

### Raw Audio & Vocal Isolation
- Gathered high-quality recordings from YouTube, ensuring variety by including both studio and live tracks.
- Isolated vocals using Ultimate Vocal Remover (UVR), achieving the cleanest vocal output.

### Audio Segmentation
- Used Whisper for precise word-level segmentation and custom Python scripts for alignment.
- Segmented audio to improve model training and alignment precision.

### Forced Alignment & Labeling
- Utilized LabelMakr for phoneme-level alignment, ensuring accurate training data for DiffSinger.

## Model Architecture

### Singing Voice Synthesis (SVS)
DiffSinger was selected due to its high-fidelity, expressive vocals. The model predicts frame-level acoustic features and generates audio using a vocoder.

**Why DiffSinger?**
- **Naturalness:** Produces expressive, high-fidelity vocals.
- **Control:** Full flexibility over pitch, duration, and phonemes.
- **Community Support:** Open-source with strong documentation.

## Data Augmentation
To enhance the training process, we applied minor data augmentations like pitch shifting and time shifting to improve model robustness and reduce overfitting.


#### Augmentation Techniques

The **DiffSinger repository** offers built-in augmentation settings:
- **Pitch shifting**: Random or fixed, ±5 semitones (default).
- **Time stretching**: 0.5x to 2.0x speed, default scale factor: 0.75.

We opted for the **default preset parameters** to maintain data integrity while adding variation.  
In addition, we manually applied further augmentations to Chester Bennington’s voice:
- **Pitch Shifting**: ±1 semitone shift (creating two new samples).
- **Loudness Adjustment**: Volume change by 10%.
- **Noise Reduction**: Mild denoising (~30% reduction) using a high-pass filter.
- **Speed Alteration**: ±10% speed change to simulate different tempos.

---

#### Training Setup

We based our work on the [openvpi DiffSinger repository](https://github.com/openvpi/DiffSinger) due to its superior documentation and added features, such as the **variance model** for better results. Training was carried out on the **LST compute cluster** at Saarland University with **HTCondor** for job scheduling.

**Key Setup**:
- **GPU Allocation**: 1 GPU, 16 GB memory per job.
- **Dependencies**: Custom conda environment (Python 3.8.20) with required packages.
- **Vocoder**: HifiGAN vocoder, fine-tuned for Chester’s voice to enhance mel-spectrogram conversion.

---

#### Model Variations

We trained **nine different models**, experimenting with varying configurations, datasets, and augmentation techniques. Key results:

##  Model Summary

- **Model 1**: Small model, 9900 epochs, used for basic testing.
- **Model 2 (Extended Small)**: 70k epochs, no significant improvement over Model 1.
- **Model 3 (Large)**: Full dataset without augmentation, 78k epochs, validation loss: 0.028.
- **Model 4 (Clean)**: Clean dataset, 52k epochs, validation loss: 0.03.
- **Model 5 (Fine-Tuned Vocoder)**: Fine-tuned HiFiGAN vocoder, 8000 epochs, validation loss: 0.007.
- **Model 6 (Variance + Acoustic)**: Pitch/tension prediction, 78k total epochs, pitch accuracy: 0.5.
- **Model 7 (Manual Cleaned)**: Manually cleaned dataset, 54k epochs, validation loss: 0.026.
- **Model 8 (Augmented Dataset)**: Augmented with pitch/time shifts, 78k epochs, validation loss: 0.01.
- **Model 9 (Augmented + Fine-Tuned Vocoder)**: Large augmented dataset with fine-tuned vocoder, 113k epochs, validation loss: 0.011.

---

#### Evaluation

## Criteria

- **Perceptual Evaluation of Speech Quality (PESQ)**: Objective Mean Opinion Score, mimics how the human ear hears sound.
- **F0 Root Mean Square Error**: Root mean square error of fundamental frequency (pitch).
- **Speech-to-noise ratio**: Ratio of speech to background noise.

---

#### Mixing & Mastering

After generating the vocals, we applied several post-processing techniques to improve the sound:
- **Noise reduction** and **volume adjustments** for better clarity.
- **Compression** to stabilize dynamics and prevent clipping.
- **Saturation** to replicate Chester Bennington's raspy, warm vocal tone.

---

# Related Repositories

These repositories are used in this project:

- [DiffSinger](https://github.com/openvpi/DiffSinger) – A deep learning model for singing voice synthesis (enhanced version with variance model support based on MoonInTheRiver)
- [DiffSinger](https://github.com/MoonInTheRiver/DiffSinger) - A deep learning model for singing voice synthesis
- [SingingVocoders](https://github.com/openvpi/SingingVocoders) – Vocoder models for singing voice synthesis  
- [nnsvs-db-converter](https://github.com/UtaUtaUtau/nnsvs-db-converter) – A tool for converting singing voice databases  
- [LabelMakr](https://github.com/spicytigermeat/LabelMakr) – A tool for generating timing labels  
- [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) – A tool for automatic text-to-speech alignment  
- [SOFA-Modded](https://github.com/Greenleaf2001/SOFA-Modded) – A modified version of SOFA with additional features
- [diffsinger-english-support](https://github.com/intunist/diffsinger-english-support) - A phoneme dictionary for DiffSinger databases
- [TextGrid2Lab](https://github.com/siship/TextGrid2Lab-Conversion) - Converter for TextGrid to Lab files
- [SingMOS](https://github.com/South-Twilight/SingMOS) - Evaluation Tool for Mean Opinion Score prediction
- [Evaluation metrics](https://github.com/SandyPanda-MLDL/-Evaluation-Metrics-Used-For-The-Performance-Evaluation-of-Voice-Conversion-VC-Models) - Performance evaluation metrics for voice conversion models





