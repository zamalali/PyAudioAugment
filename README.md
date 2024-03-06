# Audio Augmentation Tool

## Introduction
The Audio Augmentation Tool is a Python package designed to augment audio files easily, facilitating the enhancement of datasets for machine learning and data science projects related to audio processing. It utilizes the `audiomentations` library to apply various transformations like noise addition, pitch shifting, time stretching, and gain adjustment, helping improve the diversity and robustness of your audio data.

## Key Features
- **Noise Addition**: Injects Gaussian noise into audio files to simulate real-world scenarios.
- **Pitch Shifting**: Modifies the pitch of audio files without altering their duration.
- **Time Stretching**: Changes the speed and duration of audio files without affecting the pitch.
- **Gain Adjustment**: Adjusts the volume of audio files to test model sensitivity to volume variations.

## Installation
This package can be installed directly from PyPI:

```bash
pip install pyaudioaugment
```
After the installation run the following:
```bash
audio-augment
```