import os
import winsound
import matplotlib
import numpy as np
from math import ceil
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt


def singleaudio_mergeseparation(file_1,file_2,output_filename):
    #将两段音频进行合并
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


    #计算三段音频的短时傅里叶变换
    nperseg = sample_rate_1 / 50
    f1, t1, Zsamples1 = signal.stft(samples_1, fs=sample_rate_1, nperseg=nperseg)
    f2, t2, Zsamples2 = signal.stft(samples_2, fs=sample_rate_1, nperseg=nperseg)
    fmixed, tmixed, Zmixed_series = signal.stft(mixed_series, fs=sample_rate_1, nperseg=nperseg)


    # 创建掩码并应用
    Zsample = Zsamples2
    denominator = np.abs(Zmixed_series)
    numerator = np.abs(Zsample)
    mask = np.zeros_like(denominator)
    nonzero_indices = (denominator != 0)
    mask[nonzero_indices] = np.around(numerator[nonzero_indices] / denominator[nonzero_indices], 0)
    default_snr = -100  
    mask[~nonzero_indices] = default_snr

    # 将掩码应用于混合信号的时频表示
    Zsamplesmaked = np.multiply(Zmixed_series, mask)

    #将信号由频域恢复到时间域
    _, samplesrec = signal.istft(Zsamplesmaked, sample_rate_1)

    #将恢复的音频保存
    wavfile.write(output_filename, sample_rate_1, np.asarray(samplesrec, dtype=np.int16)) 




def audio_separation(file_1,file_2):
    desktop_path = os.path.expanduser('~') + '\\Desktop\\'
    output_path = desktop_path
    for i in range(2):
        input_1 = file_1 if i == 0 else file_2
        input_2 = file_2 if i == 0 else file_1
        output_filename = output_path + "recovered_" + str(2-i) + ".wav"
        singleaudio_mergeseparation(input_1, input_2, output_filename)

