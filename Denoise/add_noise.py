import numpy as np
from scipy.io import wavfile


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


#保存加噪后的文件
def save_noiseadd_file(source_file,_amplitude):
    noise_len = 2 # seconds
    wav_loc=source_file
    rate, data = wavfile.read(wav_loc)
    data = data / 32768
    noise=band_limited_noise(min_freq=4000, max_freq = 12000, samples=len(data), samplerate=rate,amplitude=_amplitude)
    noise_clip = noise[:rate*noise_len]
    audio_clip_band_limited = data+noise
    output_wav_loc = "C:\\Users\\Administrator\\Desktop\\noise.wav"
    audio_clip_band_limited_int = (audio_clip_band_limited * 32768).astype('int16')
    wavfile.write(output_wav_loc, rate, audio_clip_band_limited_int)
