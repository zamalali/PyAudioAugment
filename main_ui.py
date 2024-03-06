import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QLineEdit, QGridLayout, QSpinBox
import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, TimeStretch, Gain

# Function to load an audio file
def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr

# Define an augmentation pipeline
def get_augmentation_pipeline(noise_min, noise_max, pitch_min, pitch_max, rate_min, rate_max, gain_min, gain_max):
    return Compose([
        AddGaussianNoise(min_amplitude=noise_min, max_amplitude=noise_max, p=0.5),
        PitchShift(min_semitones=pitch_min, max_semitones=pitch_max, p=0.5),
        TimeStretch(min_rate=rate_min, max_rate=rate_max, p=0.5),
        Gain(min_gain_in_db=gain_min, max_gain_in_db=gain_max, p=0.5),
    ])

# Function to augment an audio file and save it multiple times
def augment_and_save(file_path, augment, sr, output_file_base, num_samples):
    for i in range(num_samples):
        audio, _ = load_audio(file_path)
        augmented_audio = augment(samples=audio, sample_rate=sr)
        output_file = f"{output_file_base}_augmented_{i}.wav"
        sf.write(output_file, augmented_audio, sr)

# PyQt5 GUI Class
class AudioAugmentationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle('Audio Augmentation App')
        self.layout = QGridLayout(self)
        
        # Create widgets
        self.uploadBtn = QPushButton('Upload Audio File')
        self.uploadBtn.clicked.connect(self.openFileNameDialog)
        self.fileNameLabel = QLabel('No File Selected')
        self.layout.addWidget(self.uploadBtn, 0, 0, 1, 2)
        self.layout.addWidget(self.fileNameLabel, 1, 0, 1, 2)

        self.numSamplesLabel = QLabel('Number of Samples:')
        self.numSamplesInput = QSpinBox()
        self.numSamplesInput.setMinimum(1)
        self.numSamplesInput.setMaximum(100)
        self.layout.addWidget(self.numSamplesLabel, 2, 0)
        self.layout.addWidget(self.numSamplesInput, 2, 1)

        # Manual parameter input setup
        self.noiseMinInput = QLineEdit('0.001')
        self.noiseMaxInput = QLineEdit('0.015')
        self.pitchMinInput = QLineEdit('-4')
        self.pitchMaxInput = QLineEdit('4')
        self.rateMinInput = QLineEdit('0.8')
        self.rateMaxInput = QLineEdit('1.25')
        self.gainMinInput = QLineEdit('-5')
        self.gainMaxInput = QLineEdit('5')

        # Adding parameter inputs to layout
        params = [('Noise Min:', self.noiseMinInput), ('Noise Max:', self.noiseMaxInput),
                  ('Pitch Min:', self.pitchMinInput), ('Pitch Max:', self.pitchMaxInput),
                  ('Rate Min:', self.rateMinInput), ('Rate Max:', self.rateMaxInput),
                  ('Gain Min (dB):', self.gainMinInput), ('Gain Max (dB):', self.gainMaxInput)]
        for i, (label, widget) in enumerate(params, start=3):
            self.layout.addWidget(QLabel(label), i, 0)
            self.layout.addWidget(widget, i, 1)

        # Augment button
        self.augmentBtn = QPushButton('Augment and Save')
        self.augmentBtn.clicked.connect(self.augmentAudio)
        self.layout.addWidget(self.augmentBtn, i+1, 0, 1, 2)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload Audio File", "", "Audio Files (*.wav *.mp3)", options=options)
        if fileName:
            self.fileNameLabel.setText(fileName)
            self.file_path = fileName

    def augmentAudio(self):
        if hasattr(self, 'file_path'):
            try:
                num_samples = self.numSamplesInput.value()
                noise_min = float(self.noiseMinInput.text())
                noise_max = float(self.noiseMaxInput.text())
                pitch_min = float(self.pitchMinInput.text())
                pitch_max = float(self.pitchMaxInput.text())
                rate_min = float(self.rateMinInput.text())
                rate_max = float(self.rateMaxInput.text())
                gain_min = float(self.gainMinInput.text())
                gain_max = float(self.gainMaxInput.text())

                augment = get_augmentation_pipeline(noise_min, noise_max, pitch_min, pitch_max, rate_min, rate_max, gain_min, gain_max)
                output_file_base = self.file_path.rsplit('.', 1)[0]
                _, sr = load_audio(self.file_path)
                augment_and_save(self.file_path, augment, sr, output_file_base, num_samples)
                self.fileNameLabel.setText(f'{num_samples} Augmented Files Saved')
            except Exception as e:
                self.fileNameLabel.setText(f'Error: {str(e)}')
        else:
            self.fileNameLabel.setText('Please select a file first.')

def main():
    app = QApplication(sys.argv)
    ex = AudioAugmentationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
