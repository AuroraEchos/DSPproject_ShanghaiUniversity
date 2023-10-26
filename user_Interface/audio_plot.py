import wave
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rc("font", family='SimHei')
matplotlib.rcParams['axes.unicode_minus'] = False


def plot_waveforms(file_path):
    # 读取音频文件
    wf = wave.open(file_path, "rb")
    # 获取音频参数
    params = wf.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取音频数据
    frames = wf.readframes(nframes)
    # 解码音频数据
    if sampwidth == 1:
        data = np.frombuffer(frames, dtype=np.uint8)
    elif sampwidth == 2:
        data = np.frombuffer(frames, dtype=np.int16)
    else:
        raise ValueError("Unsupported sample width")

    # 计算时间轴
    data = data[:nframes]
    time = np.arange(nframes)/framerate

    # 计算FFT,并获取频率和幅值
    freq = np.fft.fftfreq(nframes, d=1/framerate)[:int(nframes/2)]
    fft_result = np.fft.fft(data) / nframes
    mag = np.sqrt(np.real(fft_result)**2 +
                  np.imag(fft_result)**2)[:int(nframes/2)]

    # 计算对数值
    logmag = 10 * np.log10(mag)

    # 配置子图
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    # 绘制时域波形
    axs[0].plot(time, data, linewidth=0.5,color='red')
    axs[0].set_xlabel("时间(s)")
    axs[0].set_ylabel("幅度")
    axs[0].set_title("时域波形")

    # 绘制频域波形
    axs[1].plot(freq, mag,color='blue')
    axs[1].set_xlabel("频率(Hz)")
    axs[1].set_ylabel("幅度")
    axs[1].set_title("频域波形")
    axs[1].set_xlim(0, 5000)
    """ 
    # 绘制对数波形
    axs[2].plot(freq, logmag,color='green')
    axs[2].set_xlabel("频率(Hz)")
    axs[2].set_ylabel("对数(db)")
    axs[2].set_title("对数波形")
    """
    # 自适应布局，避免重叠
    fig.tight_layout()
    fig.set_dpi(78)
    fig.align_ylabels()

    # 显示图像
    plt.show()

