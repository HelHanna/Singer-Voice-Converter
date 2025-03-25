# 🎤 **Singer Voice Synthesis (SVS) with Chester Bennington's Voice**

## **Overview**
This project focuses on **Singer Voice Synthesis (SVS)** using **Chester Bennington’s voice** to generate new singing performances. The goal is to train an **SVS model** capable of generating realistic singing vocals with Chester’s unique **timbre, pitch control, vibrato, and vocal fry**.

---

## 🔍 **1. Preprocessing**
To build a high-quality dataset, we extract and prepare Chester’s vocals from existing recordings.

### 🎶 **1.1 Vocal Isolation**
- Extract **acapella vocals** from Linkin Park tracks using:
  - 🎵 **Demucs**
  - 🎵 **Spleeter**
  - 🎵 **UVR (Ultimate Vocal Remover)**
- Ensure **clean, high-fidelity audio** (48kHz, 24-bit WAV format).

### **1.2 Lyrics & Phoneme Alignment**
- Use **Montreal Forced Aligner (MFA)** to align lyrics with audio.
- Convert lyrics to **phonemes** for SVS models.

### **1.3 Feature Extraction**
- Compute **Mel Spectrograms**.
- Extract **Fundamental Frequency (F0)**.
- Generate **Speaker Embeddings** (ECAPA-TDNN, Wav2Vec).

---

## **2. Training**
To synthesize Chester’s voice, we fine-tune a **pretrained Singing Voice Synthesis (SVS) model**.

### 🧠 **2.1 Model Selection**
Choose a **pretrained SVS model** as the base:
-  **SoVITS** (Speech-to-Singing adaptation, high flexibility)
-  **Diff-SVC** (Diffusion-based SVS, high quality)
-  **X-Singer** (Advanced neural singing synthesis)

### **2.2 Data Preparation for Training**
- Train on extracted **vocal features** (spectrograms, F0, speaker embeddings).
- Use **phoneme-aligned lyrics** to improve accuracy.

### 🏋️ **2.3 Training Steps**
- Freeze early model layers, fine-tune the **timbre and phoneme duration layers**.
- Optimize loss functions:
  - **Pitch Loss** → Ensures pitch accuracy.
  - **Phoneme Duration Loss** → Improves timing.
  - **Spectral Envelope Matching** → Preserves timbre & texture.

---

##  **3. Fine-Tuning Chester’s Vocal Style**
Chester’s **aggression, vibrato, vocal fry, and roughness** require additional fine-tuning.

### 🎼 **3.1 Pitch & Timbre Fine-Tuning**
- 🎵 **Fundamental Frequency (F0) Adjustment:**
  - Learn Chester’s **pitch variations**.
  - Use **Pitch Contour Learning** to prevent robotic singing.

### 🕒 **3.2 Rhythm & Timing Adjustments**
- ⏳ **Dynamic Time Warping (DTW)** aligns generated vocals to Chester’s natural timing.
- 🔠 **Phoneme Duration Prediction** ensures correct note phrasing.

###  **3.3 Timbre & Vocal Texture Adaptation**
- **Speaker Embedding Optimization** for better timbre transfer.
- **Spectral Envelope Matching** preserves formants.
- **Style Modeling (VAE, Style Tokens)** adds vocal fry, growl, and vibrato.

---

## 🎧 **4. Inference: Generating New Vocals**
Once fine-tuning is complete, generate vocals with **Chester’s voice**.

### 📝 **4.1 Input Data**
- **Lyrics + MIDI (melody)**.
- Or **lyrics + reference vocal** for conversion-based synthesis.

### 🎚 **4.2 Post-Processing**
- Apply **EQ, reverb, compression**.
- Mix with instrumental track.


---
used resources:
# Related Repositories

These repositories are used in this project:

- [SingingVocoders](https://github.com/openvpi/SingingVocoders?tab=readme-ov-file) – Vocoder models for singing voice synthesis  
- [DiffSinger](https://github.com/openvpi/DiffSinger) – A deep learning model for singing voice synthesis  
- [nnsvs-db-converter](https://github.com/UtaUtaUtau/nnsvs-db-converter) – A tool for converting singing voice databases  
- [LabelMakr](https://github.com/spicytigermeat/LabelMakr) – A tool for generating timing labels  
- [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) – A tool for automatic text-to-speech alignment  
- [SOFA-Modded](https://github.com/Greenleaf2001/SOFA-Modded) – A modified version of SOFA with additional features  


## 📚 **6. References**
- 📄 **Pitch Contour Learning:** [PiCo-VITS](https://link.springer.com/chapter/10.1007/978-3-031-70566-3_19)
- 📄 **Dynamic Time Warping:** [SoftDTW](https://arxiv.org/abs/2304.05032)
- 📄 **Speaker Embedding Optimization:** [AlignSTS](https://aclanthology.org/2023.findings-acl.442.pdf)



