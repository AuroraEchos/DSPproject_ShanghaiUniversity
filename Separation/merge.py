import os
import numpy as np
from math import ceil
from scipy.io import wavfile
import matplotlib.pyplot as plt


def merge_files(file_1,file_2):
    sample_rate_1, samples_1 = wavfile.read(file_1)
    sample_rate_2, samples_2 = wavfile.read(file_2)
    maxlength = max(len(samples_1),len(samples_2))
    samples_1 = np.pad(samples_1, (0, maxlength - len(samples_1)), 'constant', constant_values=(0))
    samples_2 = np.pad(samples_2, (0, maxlength - len(samples_2)), 'constant', constant_values=(0))
    mixed_series = samples_1 + samples_2
    extrapadding = (ceil(len(mixed_series) / sample_rate_1) * sample_rate_1) - len(mixed_series)
    mixed_series = np.pad(mixed_series, (0,extrapadding), 'constant', constant_values=(0))
    samples_1 = np.pad(samples_1, (0,extrapadding), 'constant', constant_values=(0))
    samples_2 = np.pad(samples_2, (0,extrapadding), 'constant', constant_values=(0))


    desktop_path = os.path.expanduser('~') + '\\Desktop\\'
    filename = 'mixed.wav'
    output_wav_loc = desktop_path + filename
    wavfile.write(output_wav_loc, sample_rate_1, np.asarray(mixed_series, dtype=np.int16))
