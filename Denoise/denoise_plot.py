import librosa
import scipy.signal
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
import tkinter

matplotlib.rc("font", family='SimHei')
matplotlib.rcParams['axes.unicode_minus'] = False


def fftnoise(f):
    f = np.array(f, dtype="complex")
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1 : Np + 1] *= phases
    f[-1 : -1 - Np : -1] = np.conj(f[1 : Np + 1])
    return np.fft.ifft(f).real

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


def _stft(y, n_fft, hop_length, win_length):
    return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

def _istft(y, hop_length, win_length):
    return librosa.istft(y, hop_length=hop_length, win_length=win_length)

def _amp_to_db(x):
    return librosa.core.amplitude_to_db(x, ref=1.0, amin=1e-20, top_db=80.0)

def _db_to_amp(x,):
    return librosa.core.db_to_amplitude(x, ref=1.0)


#绘制音频信号的波形图
def plot_waveform(file_path):
    wav_loc = file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise

    output=removeNoise(audio_clip=audio_clip_band_limited,noise_clip=noise_clip)

    plt.figure(figsize=(8, 6))

    # 原始音频波形
    plt.subplot(3, 1, 1)
    plt.title("Original Audio Waveform")
    plt.plot(np.linspace(0, len(data) / rate, len(data)), data,color='black')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # 添加噪声后的音频波形
    plt.subplot(3, 1, 2)
    plt.title("Audio Waveform with Noise")
    plt.plot(np.linspace(0, len(audio_clip_band_limited) / rate, len(audio_clip_band_limited)), audio_clip_band_limited,color='black')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # 降噪后的波形图
    plt.subplot(3, 1, 3)
    plt.title("Denoised Audio Waveform")
    plt.plot(np.linspace(0, len(output) / rate, len(output)), output, color='black')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()


#绘制音频信号的频谱图
def plot_spectrogram_stft(file_path):
    wav_loc = file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    audio_clip=audio_clip_band_limited

    n_fft=2048
    hop_length=512
    win_length=2048
    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  

    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))


    fig,axs=plt.subplots(2,1,figsize=(6,4))

    cax1=axs[0].matshow(
        noise_stft_db,
        origin="lower",
        aspect="auto",
        cmap=plt.cm.seismic,
        vmin=-1 * np.max(np.abs(noise_stft_db)),
        vmax=np.max(np.abs(noise_stft_db)),
    )
    fig.colorbar(cax1)
    axs[0].set_title("噪声STFT变换")

    cax2=axs[1].matshow(
        sig_stft_db,
        origin="lower",
        aspect="auto",
        cmap=plt.cm.seismic,
        vmin=-1 * np.max(np.abs(sig_stft_db)),
        vmax=np.max(np.abs(sig_stft_db)),
    )
    fig.colorbar(cax2)
    axs[1].set_title("信号STFT变换")

    plt.tight_layout()
    plt.show()

def plot_spectrogram_mask(file_path):

    wav_loc = file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    audio_clip=audio_clip_band_limited

    n_fft=2048
    hop_length=512
    win_length=2048
    n_std_thresh=1.5
    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  

    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))

    mask_gain_dB = np.min(_amp_to_db(np.abs(sig_stft)))

    n_grad_freq=2
    n_grad_time=4

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

    db_thresh = np.repeat(np.reshape(noise_thresh, [1, len(mean_freq_noise)]),np.shape(sig_stft_db)[1],axis=0,).T

    sig_mask = sig_stft_db < db_thresh

    prop_decrease=1.0
    sig_mask = scipy.signal.fftconvolve(sig_mask, smoothing_filter, mode="same")
    sig_mask = sig_mask * prop_decrease

    sig_stft_db_masked = (sig_stft_db * (1 - sig_mask)+ np.ones(np.shape(mask_gain_dB)) * mask_gain_dB * sig_mask)


    fig,axs=plt.subplots(2,1,figsize=(6,4))
    
    cax1=axs[0].matshow(
        sig_mask,
        origin="lower",
        aspect="auto",
        cmap=plt.cm.seismic,
        vmin=-1 * np.max(np.abs(sig_mask)),
        vmax=np.max(np.abs(sig_mask)),
    )
    fig.colorbar(cax1)
    axs[0].set_title("应用遮罩")

    cax2=axs[1].matshow(
        sig_stft_db_masked,
        origin="lower",
        aspect="auto",
        cmap=plt.cm.seismic,
        vmin=-1 * np.max(np.abs(sig_stft_db_masked)),
        vmax=np.max(np.abs(sig_stft_db_masked)),
    )
    fig.colorbar(cax2)
    axs[1].set_title("遮蔽信号")

    plt.tight_layout()
    plt.show()

def plot_spectrogram_recovered(file_path):

    wav_loc = file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    audio_clip=audio_clip_band_limited

    n_fft=2048
    hop_length=512
    win_length=2048
    n_std_thresh=1.5
    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  

    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))

    mask_gain_dB = np.min(_amp_to_db(np.abs(sig_stft)))

    n_grad_freq=2
    n_grad_time=4

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

    db_thresh = np.repeat(np.reshape(noise_thresh, [1, len(mean_freq_noise)]),np.shape(sig_stft_db)[1],axis=0,).T

    sig_mask = sig_stft_db < db_thresh

    prop_decrease=1.0
    sig_mask = scipy.signal.fftconvolve(sig_mask, smoothing_filter, mode="same")
    sig_mask = sig_mask * prop_decrease

    sig_stft_db_masked = (sig_stft_db * (1 - sig_mask)+ np.ones(np.shape(mask_gain_dB)) * mask_gain_dB * sig_mask)

    sig_imag_masked = np.imag(sig_stft) * (1 - sig_mask)
    sig_stft_amp = (_db_to_amp(sig_stft_db_masked) * np.sign(sig_stft)) + (1j * sig_imag_masked)


    recovered_signal = _istft(sig_stft_amp, hop_length, win_length)
    recovered_spec = _amp_to_db(np.abs(_stft(recovered_signal, n_fft, hop_length, win_length)))


    fig, ax = plt.subplots(figsize=(6, 4))
    cax = ax.matshow(
        recovered_spec,
        origin="lower",
        aspect="auto",
        cmap=plt.cm.seismic,
        vmin=-1 * np.max(np.abs(recovered_spec)),
        vmax=np.max(np.abs(recovered_spec)),
    )
    fig.colorbar(cax)
    ax.set_title("恢复的频谱图")
    plt.tight_layout()
    plt.show()


#两个子图，其中包括了统计信息和一个平滑掩码（filter）的图形
def plot_statistics_and_filter(file_path):

    wav_loc = file_path
    rate, data = wavfile.read(wav_loc)
    data = data / 32768

    noise_len = 2 # seconds
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=5)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    audio_clip=audio_clip_band_limited

    n_fft=2048
    hop_length=512
    win_length=2048
    n_std_thresh=1.5
    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  

    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))

    mask_gain_dB = np.min(_amp_to_db(np.abs(sig_stft)))

    n_grad_freq=2
    n_grad_time=4

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

    fig, axs = plt.subplots(ncols=2, figsize=(6, 4))
    
    plt_mean, = axs[0].plot(mean_freq_noise, label="噪声均值")
    plt_std, = axs[0].plot(std_freq_noise, label="噪声标准差")
    plt_std, = axs[0].plot(noise_thresh, label="噪声阈值")
    axs[0].set_title("掩码阈值")
    axs[0].legend()
    
    cax = axs[1].matshow(smoothing_filter, origin="lower")
    fig.colorbar(cax)
    axs[1].set_title("平滑掩码")
    
    plt.tight_layout()
    plt.show()


def denoise_plot(file_path):
    denoise_window = tk.Toplevel()
    denoise_window.geometry("300x200")
    denoise_window.resizable(0, 0)
    denoise_window.title("降噪可视化")
    denoise_window.iconbitmap("user_Interface\\icon\\001.ico")

    b1=tkinter.Button(denoise_window, text="waveform", width=20, activebackground='blue',command=lambda:[plot_waveform(file_path)])
    b1.place(x=80,y=10)
    b2=tkinter.Button(denoise_window, text="spectrogram_stft", width=20, activebackground='blue',command=lambda:[plot_spectrogram_stft(file_path)])
    b2.place(x=80,y=45)
    b3=tkinter.Button(denoise_window, text="spectrogram_mask", width=20, activebackground='blue',command=lambda:[plot_spectrogram_mask(file_path)])
    b3.place(x=80,y=80)
    b4=tkinter.Button(denoise_window, text="statistics_and_filter", width=20, activebackground='blue',command=lambda:[plot_statistics_and_filter(file_path)])
    b4.place(x=80,y=115)
    b5=tkinter.Button(denoise_window, text="spectrogram_recovered", width=20, activebackground='blue',command=lambda:[plot_spectrogram_recovered(file_path)])
    b5.place(x=80,y=150)

    denoise_window.mainloop()
