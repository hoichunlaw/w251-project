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
import librosa
import librosa.display
import collections


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
q = queue.Queue()
mpl.use('TKAgg', force=True)
fig, ax = plt.subplots()
d = collections.deque(maxlen=10000)

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    # if status:
    #     print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])

try:
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    with stream:
        try:
            while True:
                # print("stream params", stream.blocksize, stream.samplerate, stream.samplesize, stream.latency)
                sd.sleep(3 * 1000)
                data_raw = [(q.get_nowait()).flatten() for i in range(q.qsize())]
                d.extend(data_raw)
                frames = (np.hstack(d)).flatten()
                melspec = librosa.feature.melspectrogram(y=frames, sr=stream.samplerate, n_mels=128, fmax=4000)
                print(f"Frames array: {frames.shape}, Melspec array: {melspec.shape}")
                data_out = librosa.core.power_to_db(melspec, ref=np.max)
                librosa.display.specshow(data_out, y_axis='mel', fmax=4000, x_axis='time')
                plt.draw()
                plt.pause(0.0001)
                plt.clf()
        except KeyboardInterrupt:
            pass

except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
