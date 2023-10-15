import os
import librosa
import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from datetime import timedelta as td


#对输入的频域进行噪声添加
def fftnoise(f):
    f = np.array(f, dtype="complex")
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1 : Np + 1] *= phases
    f[-1 : -1 - Np : -1] = np.conj(f[1 : Np + 1])
    return np.fft.ifft(f).real


#产生一定频率范围内的噪声
def band_limited_noise(min_freq, max_freq,samples, samplerate,amplitude):
    freqs = np.abs(np.fft.fftfreq(samples, 1 / samplerate))
    f = np.zeros(samples)
    f[np.logical_and(freqs >= min_freq, freqs <= max_freq)] = 1
    noise = fftnoise(f)
    amplitude_=amplitude
    return amplitude_ * noise


def removeNoise(audio_clip,noise_clip):
    
    n_grad_freq=2
    n_grad_time=4
    n_fft=2048
    win_length=2048
    hop_length=512
    n_std_thresh=1.5
    prop_decrease=1.0

    def _stft(y, n_fft, hop_length, win_length):
        return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    def _istft(y, hop_length, win_length):
        return librosa.istft(y, hop_length=hop_length, win_length=win_length)

    def _amp_to_db(x):
        return librosa.core.amplitude_to_db(x, ref=1.0, amin=1e-20, top_db=80.0)

    def _db_to_amp(x,):
        return librosa.core.db_to_amplitude(x, ref=1.0)

    # step 1 噪声的STFT变换
    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  

    # step 2 计算噪声的统计特征
    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    # step 3 信号的STFT变换
    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))

    # step 4 计算遮罩的增益值
    mask_gain_dB = np.min(_amp_to_db(np.abs(sig_stft)))

    # step 5 创建时间和频率上的平滑滤波器
    smoothing_filter = np.outer(
        np.concatenate(
            [
                np.linspace(0, 1, n_grad_freq + 1, endpoint=False),
                np.linspace(1, 0, n_grad_freq + 2),
            ]
        )[1:-1],
        np.concatenate(
            [
                np.linspace(0, 1, n_grad_time + 1, endpoint=False),
                np.linspace(1, 0, n_grad_time + 2),
            ]
        )[1:-1],
    )
    smoothing_filter = smoothing_filter / np.sum(smoothing_filter)

    # step 6 计算每个频率/时间点的阈值
    db_thresh = np.repeat(np.reshape(noise_thresh, [1, len(mean_freq_noise)]),np.shape(sig_stft_db)[1],axis=0,).T

    # step 7 如果信号高于阈值，则进行遮罩处理
    sig_mask = sig_stft_db < db_thresh

    # step 8 使用平滑滤波器对遮罩进行卷积
    sig_mask = scipy.signal.fftconvolve(sig_mask, smoothing_filter, mode="same")
    sig_mask = sig_mask * prop_decrease

    # step 9 对信号进行遮蔽处理
    sig_stft_db_masked = (sig_stft_db * (1 - sig_mask)+ np.ones(np.shape(mask_gain_dB)) * mask_gain_dB * sig_mask)

    # step 10 遮蔽实部
    sig_imag_masked = np.imag(sig_stft) * (1 - sig_mask)
    sig_stft_amp = (_db_to_amp(sig_stft_db_masked) * np.sign(sig_stft)) + (1j * sig_imag_masked)

    # step 11 恢复信号
    recovered_signal = _istft(sig_stft_amp, hop_length, win_length)
    recovered_spec = _amp_to_db(np.abs(_stft(recovered_signal, n_fft, hop_length, win_length)))

    return recovered_signal


def audio_removenoise(file_path):
    wav_loc=file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    desktop_path = os.path.expanduser('~') + '\\Desktop\\'

    filename_1 = 'noise.wav'
    output_wav_loc = desktop_path + filename_1
    audio_clip_band_limited_int = (audio_clip_band_limited * 32768).astype('int16')
    wavfile.write(output_wav_loc, rate, audio_clip_band_limited_int)

    output=removeNoise(audio_clip=audio_clip_band_limited,noise_clip=noise_clip)

    filename_2 = 'denoised.wav'
    output_wav_loc_denoised = desktop_path + filename_2
    output_denoised_int = (output * 32768).astype('int16')
    wavfile.write(output_wav_loc_denoised, rate, output_denoised_int)


