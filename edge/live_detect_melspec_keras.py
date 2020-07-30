#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from PIL import Image
import librosa
import librosa.display as display
from kapre.time_frequency import Melspectrogram
import collections
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import os

IM_SIZE = (224,224,3)
input_saved_model_dir = '/home/carlos/w251-project/models/imgnet_mobilenet_v2_140_224/Fri_Jul_24_02_35_06_2020'
BIRDS = ["amered",  "annhum",  "belkin1",  "blugrb1",  "brthum", "cedwax",  "commer",  "gockin",  "gryfly",  "horlar",
         "moudov",  "olsfly",  "pasfly",  "semsan",  "sposan", "vigswa",  "wewpew",  "whbnut",  "wilsni1",  "yelwar"]

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

mpl.use('TKAgg', force=True)
fig, ax = plt.subplots()
q = queue.Queue()
d = collections.deque(maxlen=10000)
the_model = tf.keras.models.load_model(input_saved_model_dir)
print(the_model.summary())

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    # if status:
    #     print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])

def my_decode_predictions(classes, preds, top=5):
  results = []
  for pred in preds:
    top_indices = pred.argsort()[-top:][::-1]
    result = [[classes[i], pred[i]] for i in top_indices]
    result.sort(key=lambda x: x[1], reverse=True)
    results.append(result)
  return results

try:
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    with stream:
        try:
            while True:
                # print("stream params", stream.blocksize, stream.samplerate, stream.samplesize, stream.latency)
                sr=stream.samplerate
                sd.sleep(3 * 1000)
                data_raw = [(q.get_nowait()).flatten() for i in range(q.qsize())]
                d.extend(data_raw)
                frames = (np.hstack(d)).flatten()
                melspec = Melspectrogram(n_dft=1024, 
                                    n_hop=256,
                                    input_shape=(1, frames.shape[0]),
                                    padding='same', sr=sr, n_mels=224, fmin=1400, fmax=sr/2,
                                    power_melgram=2.0, return_decibel_melgram=True,
                                    trainable_fb=False, trainable_kernel=False)(frames.reshape(1, 1, -1)).numpy()
                melspec = melspec.reshape(melspec.shape[1], melspec.shape[2])
                print(f"Frames array: {frames.shape}, Melspec array: {melspec.shape}")
                melplot = display.specshow(melspec, sr=sr)
                melplot.set_frame_on(False)
                plt.tight_layout(pad=0)
                plt.draw()
                plt.pause(0.0001)
                plt.clf()
                if (melspec.shape[1] >= IM_SIZE[0]):
                    img=Image.frombuffer("RGBA", fig.canvas.get_width_height(),
                         fig.canvas.buffer_rgba(), "raw", "RGBA", 0, 1)
                    img = img.convert('RGB').resize(IM_SIZE[0:2])
                    x = keras_image.img_to_array(img)
                    # print(f"image shape: {x.shape}")
                    x = preprocess_input(np.expand_dims(x, axis=0))
                    preds = the_model.predict(x)
                    print(f'\nPredicted: {my_decode_predictions(BIRDS, preds, top=5)[0]}\n')

        except KeyboardInterrupt:
            pass

except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))


# # Optional image to test model prediction.
# img_path = './aldfly1.png'

# # Load the image for prediction.
# img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_HEIGHT))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)

# preds = the_model.predict(x)
# # decode the results into a list of tuples (class, probability)
# print('Predicted:', my_decode_predictions(BIRDS, preds, top=20)[0])