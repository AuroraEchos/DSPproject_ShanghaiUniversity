import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from matplotlib.patches import Rectangle

def denoise_plot():
    desktop_path = os.path.expanduser('~') + '\\Desktop\\'

    original_audio = desktop_path + "original_audio.wav"
    noisy_audio = desktop_path + "noise_audio.wav"
    denoised_audio = desktop_path + "denoised_audio.wav"

    sample_rate_original, audio_data_original = wavfile.read(original_audio)
    sample_rate_noisy, audio_data_noisy = wavfile.read(noisy_audio)
    sample_rate_denoised, audio_data_denoised = wavfile.read(denoised_audio)

    # 创建一个6x2的子图布局，分为三行两列
    fig, axs = plt.subplots(3, 2, figsize=(8, 6))

    # 调整子图的布局以留出空隙
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # 绘制原音频的频谱图和波形图
    axs[0, 0].specgram(audio_data_original, Fs=sample_rate_original, cmap='viridis')
    axs[0, 0].set_title("Original Audio (Spectrogram)")
    axs[0, 1].plot(audio_data_original, color='black')
    axs[0, 1].set_title("Original Audio (Waveform)")

    # 绘制加噪后的音频的频谱图和波形图
    axs[1, 0].specgram(audio_data_noisy, Fs=sample_rate_noisy, cmap='viridis')
    axs[1, 0].set_title("Noisy Audio (Spectrogram)")
    axs[1, 1].plot(audio_data_noisy, color='black')
    axs[1, 1].set_title("Noisy Audio (Waveform)")

    # 绘制降噪后的音频的频谱图和波形图
    axs[2, 0].specgram(audio_data_denoised, Fs=sample_rate_denoised, cmap='viridis')
    axs[2, 0].set_title("Denoised Audio (Spectrogram)")
    axs[2, 1].plot(audio_data_denoised, color='black')
    axs[2, 1].set_title("Denoised Audio (Waveform)")

    # 关闭坐标轴
    for ax in axs.flat:
        ax.set_axis_off()

    # 调整子图的背景颜色为浅色
    for ax in axs.flat:
        ax.set_facecolor('lightgray')

    # 在每个子图周围添加一个白色矩形框
    for ax in axs.flat:
        rect = Rectangle((0, 0), 1, 1, fill=False, edgecolor='black', lw=0)
        ax.add_patch(rect)
    
    # 调整布局以确保子图不重叠
    plt.tight_layout()
    plt.show()
