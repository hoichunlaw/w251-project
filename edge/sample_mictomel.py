#import cv2
import numpy as np
import pyaudio
import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

rate = 16000
chunk_size = rate // 4


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=22,
                frames_per_buffer=chunk_size)

print(10)
frames = []

plt.figure(figsize=(10, 4))
do_melspec = librosa.feature.melspectrogram
pwr_to_db = librosa.core.power_to_db

while True:

    mpl.use('TKAgg', force=True)
    start = time.time()

    data = stream.read(chunk_size)
    data = np.fromstring(data, dtype=np.float32)

    melspec = do_melspec(y=data, sr=rate, n_mels=128, fmax=4000)
    norm_melspec = pwr_to_db(melspec, ref=np.max)

    frames.append(norm_melspec)
    
    if len(frames) == 20:
        
        stack = np.hstack(frames)
        
        librosa.display.specshow(stack, y_axis='mel', fmax=4000, x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        #break
        frames.pop(0)


    t = time.time() - start

    print(f"Waiting...{1 / t}")