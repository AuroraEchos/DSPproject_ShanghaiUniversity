import os
import wave  
import math  
import numpy as np  
from scipy.special import expn  
import matplotlib.pyplot as plt  
from scipy.io.wavfile import read, write  


# 将音频数据转换为浮点数格式以便处理
def to_float(_input):
    if _input.dtype == np.float64:
        return _input, _input.dtype
    elif _input.dtype == np.float32:
        return _input.astype(np.float64), _input.dtype
    elif _input.dtype == np.uint8:
        return (_input - 128) / 128., _input.dtype
    elif _input.dtype == np.int16:
        return _input / 32768., _input.dtype
    elif _input.dtype == np.int32:
        return _input / 2147483648., _input.dtype
    raise ValueError('Unsupported wave file format, please contact the author')

# 将浮点数数据还原为原始格式
def from_float(_input, dtype):
    if dtype == np.float64:
        return _input, np.float64
    elif dtype == np.float32:
        return _input.astype(np.float32)
    elif dtype == np.uint8:
        return ((_input * 128) + 128).astype(np.uint8)
    elif dtype == np.int16:
        return (_input * 32768).astype(np.int16)
    elif dtype == np.int32:
        print(_input)
        return (_input * 2147483648).astype(np.int32)
    raise ValueError('Unsupported wave file format, please contact the author')

# 主要的音频降噪函数，接受音频数据、采样率和其他可选参数
def logmmse(data, sampling_rate, output_file=None, initial_noise=6, window_size=0, noise_threshold=0.15):
    data, dtype = to_float(data)        # 将音频数据转换为浮点数
    data += np.finfo(np.float64).eps    # 添加一个极小的值以避免除以零

    if data.ndim == 1:  # 如果是单声道音频
        output = mono_logmmse(data, sampling_rate, dtype, initial_noise, window_size, noise_threshold)
    else:               # 如果是多通道音频
        output = []
        for _, m_input in enumerate(data.T):  # 遍历每个通道
            output.append(mono_logmmse(m_input, sampling_rate, dtype, initial_noise, window_size, noise_threshold))
        output = np.array(output)

    if output_file is not None:                      # 如果提供了输出文件名
        write(output_file, sampling_rate, output.T)  # 将处理后的音频写入文件

    return output.T  # 返回处理后的音频数据

# 从文件中读取音频数据并应用logmmse降噪
def logmmse_from_file(input_file, output_file=None, initial_noise=6, window_size=0, noise_threshold=0.15):
    sampling_rate, data = read(input_file, 'r') 
    return logmmse(data, sampling_rate, output_file, initial_noise, window_size, noise_threshold)

# 对单声道音频进行LogMMSE降噪
def mono_logmmse(m_input, fs, dtype, initial_noise=6, window_size=0, noise_threshold=0.15):
    num_frames = len(m_input)
    chunk_size = int(np.floor(60 * fs))
    m_output = np.array([], dtype=dtype)
    saved_params = None
    frames_read = 0

    while frames_read < num_frames:
        frames = num_frames - frames_read if frames_read + chunk_size > num_frames else chunk_size
        signal = m_input[frames_read:frames_read + frames]
        frames_read = frames_read + frames
        _output, saved_params = _logmmse(signal, fs, initial_noise, window_size, noise_threshold, saved_params)
        m_output = np.concatenate((m_output, from_float(_output, dtype)))

    return m_output  # 返回处理后的音频数据

# 实际执行LogMMSE降噪的内部函数
def _logmmse(x, Srate, noise_frames=6, Slen=0, eta=0.15, saved_params=None):
    if Slen == 0:               # 如果未提供分析窗口长度，则默认使用20毫秒的分析窗口
        Slen = int(math.floor(0.02 * Srate))
    if Slen % 2 == 1:           # 确保分析窗口长度为偶数
        Slen = Slen + 1
    PERC = 50
    len1 = int(math.floor(Slen * PERC / 100))
    len2 = int(Slen - len1)
    win = np.hanning(Slen)
    win = win * len2 / np.sum(win)
    nFFT = 2 * Slen
    x_old = np.zeros(len1)
    Xk_prev = np.zeros(len1)
    Nframes = int(math.floor(len(x) / len2) - math.floor(Slen / len2))
    xfinal = np.zeros(Nframes * len2)

    if saved_params is None:  # 如果未提供已保存的参数，初始化噪声均值估计
        noise_mean = np.zeros(nFFT)
        for j in range(0, Slen * noise_frames, Slen):
            noise_mean = noise_mean + np.absolute(np.fft.fft(win * x[j:j + Slen], nFFT, axis=0))
        noise_mu2 = (noise_mean / noise_frames) ** 2
    else:
        noise_mu2 = saved_params['noise_mu2']
        Xk_prev = saved_params['Xk_prev']
        x_old = saved_params['x_old']
    
    aa = 0.98
    mu = 0.98
    ksi_min = 10 ** (-25 / 10)

    for k in range(0, Nframes * len2, len2):        # 遍历音频数据的每个帧
        insign = win * x[k:k + Slen]                # 分帧处理

        spec = np.fft.fft(insign, nFFT, axis=0)     # 计算信号频谱
        sig = np.absolute(spec)
        sig2 = sig ** 2

        gammak = np.minimum(sig2 / noise_mu2, 40)   # 估计信噪比（SNR）

        if Xk_prev.all() == 0:
            ksi = aa + (1 - aa) * np.maximum(gammak - 1, 0)
        else:
            ksi = aa * Xk_prev / noise_mu2 + (1 - aa) * np.maximum(gammak - 1, 0)
            ksi = np.maximum(ksi_min, ksi)

        log_sigma_k = gammak * ksi / (1 + ksi) - np.log(1 + ksi)    # 计算对数谱
        vad_decision = np.sum(log_sigma_k) / Slen                   # 基于VAD决策更新噪声估计

        if vad_decision < eta:
            noise_mu2 = mu * noise_mu2 + (1 - mu) * sig2

        A = ksi / (1 + ksi)
        vk = A * gammak
        ei_vk = 0.5 * expn(1, vk)
        hw = A * np.exp(ei_vk)
        sig = sig * hw
        Xk_prev = sig ** 2
        xi_w = np.fft.ifft(hw * spec, nFFT, axis=0)
        xi_w = np.real(xi_w)

        xfinal[k:k + len2] = x_old + xi_w[0:len1]
        x_old = xi_w[len1:Slen]

    return xfinal, {'noise_mu2': noise_mu2, 'Xk_prev': Xk_prev, 'x_old': x_old}



# 算法调用函数
def denoise(audio_path):
    path = audio_path
    f = wave.open(path, "rb")
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    data = f.readframes(nframes)
    f.close()
    data = np.frombuffer(data, dtype=np.short)

    data = logmmse(data=data, sampling_rate=framerate)  # 调用logmmse函数降噪


    desktop_path = os.path.expanduser('~') + '\\Desktop\\'
    filename = 'denoised_audio.wav'
    file_save = desktop_path + filename
    nframes = len(data)
    f = wave.open(file_save, 'wb')
    f.setparams((1, 2, framerate, nframes, 'NONE', 'NONE'))
    f.writeframes(data)
    f.close()

    return data


""" 
    # 读取原始音频
    desktop_path = os.path.expanduser('~') + '\\Desktop\\'
    filename = 'noise.wav'
    path_original = desktop_path + filename
    f_original = wave.open(path_original, "rb")
    data_original = f_original.readframes(nframes)
    f_original.close()
    data_original = np.frombuffer(data_original, dtype=np.short)

    # 绘制原始音频波形
    plt.figure(figsize=(12, 6))
    plt.subplot(211)
    plt.title("Original Audio")
    plt.plot(data_original, color='black')

    # 绘制降噪后的音频波形
    plt.subplot(212)
    plt.title("Denoised Audio")
    plt.plot(data, color='black')

    plt.tight_layout()
    plt.show()

 """



""" 
步骤： 
    1、音频数据准备:        首先从.wav文件中读取音频数据，并将其转换为浮点数格式以便后续处理。
    2、初始处理:            进行初始的参数设定，包括采样率、初始噪声估计、窗口大小等。
    3、分帧处理:            将音频数据分帧，每帧的大小通常为20毫秒。对每个帧应用汉宁窗以平滑信号。
    4、信号频谱计算:        对每个窗口内的音频数据进行快速傅立叶变换（FFT），计算信号的频谱。
    5、信噪比估计:          计算信号帧的信噪比，以区分信号和噪声成分。
    6、对数谱计算:          基于信噪比，计算对数谱来进一步增强信号成分，减弱噪声。
    7、VAD决策:             使用VAD（Voice Activity Detection）决策，判断当前帧是否包含语音信号。
    8、噪声估计更新:        如果VAD决策表明当前帧为噪声帧，根据决策结果更新噪声估计。
    9、对数谱增强:          使用对数谱增强信号。
    10、频谱还原:           将增强后的频谱通过逆FFT还原为时域信号。
    11、信号合成:           将相邻帧的音频信号进行合成，以获取降噪后的音频数据。
    12、保存处理后的音频:    将处理后的音频数据保存到新的.wav文件。

"""