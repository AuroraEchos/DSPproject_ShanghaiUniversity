import os
import winsound
import matplotlib
import numpy as np
from math import ceil
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

matplotlib.rc("font", family='SimHei')
matplotlib.rcParams['axes.unicode_minus'] = False


def separation_plot_1(file_1,file_2):
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
    sample = samples_2
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

    def mixed_image(ax):
        # 绘制三段音频的图像
        x = np.arange(0, len(mixed_series) / sample_rate_1, 1 / sample_rate_1)
        ax.plot(x, samples_1, color="blue", alpha=0.6)
        ax.plot(x, samples_2, color="red", alpha=0.6)
        ax.set(xlabel='时间 [秒]', ylabel='振幅')
        ax.legend(['信号1', '信号2'])

    def spectrogram_image(ax):
        # 绘制三段音频的振幅、频谱图
        ax.pcolormesh(t1, f1, np.abs(Zsamples1))
        ax.set(title='信号 1', xlabel='时间 [秒]')

    def mask_image(ax):
        # 掩码图像
        masked_values = np.ma.masked_where(mask == default_snr, mask)
        ax.imshow(masked_values, cmap='Greys', interpolation='none', vmin=0, vmax=1)

    def comparison_image_sample_1(ax):
        x = np.arange(0, len(mixed_series) / sample_rate_1, 1 / sample_rate_1)
        ax.plot(x, sample, color="red", alpha=0.6)
        ax.plot(x, samplesrec, color="blue", alpha=0.4)
        ax.set(xlabel='时间 [秒]', ylabel='信号')
        ax.legend(['原始信号', '恢复信号'])


    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    mixed_image(axes[0])
    mask_image(axes[1])
    comparison_image_sample_1(axes[2])
    plt.tight_layout()
    # 保存图像到文件
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    mask_path = os.path.join(desktop_path, "Dsp", "Separation", "scratch_file", "mask_plot_1.png")
    axes[1].figure.savefig(mask_path)
    plt.close(axes[1].figure)  # 关闭图像窗口


def separation_plot_2(file_1,file_2):
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
    sample = samples_2
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

    def mixed_image(ax):
        # 绘制三段音频的图像
        x = np.arange(0, len(mixed_series) / sample_rate_1, 1 / sample_rate_1)
        ax.plot(x, samples_1, color="blue", alpha=0.6)
        ax.plot(x, samples_2, color="red", alpha=0.6)
        ax.set(xlabel='时间 [秒]', ylabel='振幅')
        ax.legend(['信号1', '信号2'])

    def spectrogram_image(ax):
        # 绘制三段音频的振幅、频谱图
        ax.pcolormesh(t1, f1, np.abs(Zsamples1))
        ax.set(title='信号 1', xlabel='时间 [秒]')

    def mask_image(ax):
        # 掩码图像
        masked_values = np.ma.masked_where(mask == default_snr, mask)
        ax.imshow(masked_values, cmap='Greys', interpolation='none', vmin=0, vmax=1)

    def comparison_image_sample_1(ax):
        x = np.arange(0, len(mixed_series) / sample_rate_1, 1 / sample_rate_1)
        ax.plot(x, sample, color="red", alpha=0.6)
        ax.plot(x, samplesrec, color="blue", alpha=0.4)
        ax.set(xlabel='时间 [秒]', ylabel='信号')
        ax.legend(['原始信号', '恢复信号'])


    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    mixed_image(axes[0])
    mask_image(axes[1])
    comparison_image_sample_1(axes[2])
    plt.tight_layout()
    # 保存图像到文件
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    mask_path = os.path.join(desktop_path, "Dsp", "Separation", "scratch_file", "mask_plot_2.png")
    axes[1].figure.savefig(mask_path)
    plt.close(axes[1].figure)  # 关闭图像窗口


def show_audio_separation_results(file_1, file_2):
    # 调用 separation_plot_1 和 separation_plot_2 生成两张图片
    separation_plot_1(file_1=file_1, file_2=file_2)
    separation_plot_2(file_1=file_2, file_2=file_1)
    
    # 读取这两张图片并存储到一个列表中
    images = []
    titles = ["Mask - Plot 1", "Mask - Plot 2"]
    for i in range(1, 3):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        img_path = os.path.join(desktop_path, "Dsp", "Separation", "scratch_file", f"mask_plot_{i}.png")
        img = plt.imread(img_path)
        images.append(img)
    
    # 在一个图中显示两张图片
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    
    for i, ax in enumerate(axes):
        ax.imshow(images[i], cmap='gray', extent=[0, 1, 0, 1], aspect='auto')
        ax.set_title(titles[i])
        ax.axis('off')
    
    plt.subplots_adjust(left=0.05, right=0.95, wspace=0.05)
    
    plt.show()

