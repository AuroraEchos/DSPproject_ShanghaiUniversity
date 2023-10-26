import os
import numpy as np
import pandas as pd
from PIL import Image
from scipy import signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.silence import split_on_silence


audio_folder = "Recognition\\datasets\\audio"
img_folder   = "Recognition\\datasets\\img"
output_file  = "Recognition\\datasets\\attributes\\image_attributes.txt"
text_path    = "Recognition\\datasets\\attributes\\image_attributes.txt"



def statistics(text_path):
    data = pd.read_csv(text_path, delimiter=":", header=None, encoding='GBK')
    data.columns = ['属性', '值']

    # 分辨率统计
    resolution_data = data[data['属性'].str.strip() == '分辨率']
    resolution_values = resolution_data['值'].str.strip().str.split('x', expand=True).astype(int)
    average_resolution = resolution_values.mean()
    max_resolution = resolution_values.max()
    min_resolution = resolution_values.min()

    # 颜色模式统计
    color_mode_data = data[data['属性'].str.strip() == '颜色模式']
    color_mode_counts = color_mode_data['值'].str.strip().value_counts()

    # 文件格式统计
    file_format_data = data[data['属性'].str.strip() == '文件格式']
    file_format_counts = file_format_data['值'].str.strip().value_counts()

    # 文件大小统计
    file_size_data = data[data['属性'].str.strip() == '文件大小']
    file_size_values = file_size_data['值'].str.strip().str.extract('(\d+)').astype(int)
    average_file_size = file_size_values.mean()
    max_file_size = file_size_values.max()
    min_file_size = file_size_values.min()


    # 定义保存统计信息的txt文件路径
    output_stats_file = "Recognition\\datasets\\attributes\\image_statistics.txt"

    # 写入统计信息到txt文件
    with open(output_stats_file, 'w') as file:
        file.write("分辨率统计:\n")
        file.write(f"平均分辨率: {average_resolution}\n")
        file.write(f"最大分辨率: {max_resolution}\n")
        file.write(f"最小分辨率: {min_resolution}\n\n")

        file.write("颜色模式统计:\n")
        file.write(f"{color_mode_counts}\n\n")

        file.write("文件格式统计:\n")
        file.write(f"{file_format_counts}\n\n")

        file.write("文件大小统计:\n")
        file.write(f"平均文件大小: {average_file_size} bytes\n")
        file.write(f"最大文件大小: {max_file_size} bytes\n")
        file.write(f"最小文件大小: {min_file_size} bytes\n")


def img_attributes(img_folder):
    with open(output_file,'w') as file:
        for filename in os.listdir(img_folder):
            if filename.endswith(".png"):
                file_path = os.path.join(img_folder,filename)
                image = Image.open(file_path)

                width, height   = image.size                    # 频谱图宽度、高度
                num_channels    = len(image.getbands())         # 频谱图颜色通道数
                image_mode      = image.mode                    # 图像的颜色模式
                image_format    = image.format                  # 图像的文件格式
                image_size      = os.path.getsize(file_path)    # 图像文件大小（字节）

                file.write(f"文件名:        {filename}\n")
                file.write(f"分辨率:        {width} x {height}\n")
                file.write(f"颜色模式:      {image_mode}\n")
                file.write(f"文件格式:      {image_format}\n")
                file.write(f"文件大小:      {image_size} bytes\n")
                file.write(f"颜色通道数:    {num_channels}\n")
                file.write("-" * 30 + "\n")  


def channel_process(img_folder):
    for filename in os.listdir(img_folder):
        if filename.endswith(".png"):
            file_path = os.path.join(img_folder, filename)
            image = Image.open(file_path)
            image = image.convert('RGB') 
            save_path = "Recognition\\datasets\\img\\"
            file_name = filename
            save_img  = os.path.join(save_path,file_name)
            image.save(save_img)
            print("正在处理频谱图：",file_name)


def label(img_folder):
    audio_files = os.listdir(img_folder)
    labels = [file.split('_')[0] for file in audio_files]
    label_df = pd.DataFrame({'Filename': audio_files, 'Label': labels})
    label_df.to_csv("Recognition\\datasets\\label\\labels.csv", index=False)


def mute_processing(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    background_noise = audio.dBFS
    min_silence_len = 100
    silence_threshold = background_noise - 10
    segments = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)
    non_silent_audio = AudioSegment.empty()
    for segment in segments:
        non_silent_audio += segment

    return non_silent_audio


def spec(audio_folder):
    for filename in os.listdir(audio_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(audio_folder, filename)

            sample_rate = mute_processing(audio_file = file_path).frame_rate
            audio_data = np.array(mute_processing(audio_file=file_path).get_array_of_samples())

            f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate, nperseg=512, noverlap=256, nfft=1024)
            save_path = "Recognition\\datasets\\img\\"
            file_name = filename.replace(".wav",".png")
            save_img  = os.path.join(save_path,file_name)
            plt.figure(figsize=(8, 6))
            plt.pcolormesh(t, f, 10 * np.log10(Sxx))
            plt.axis('off') 
            plt.savefig(save_img, bbox_inches='tight', pad_inches=0, dpi=256, format='png', transparent=False)
            plt.close()

            print("正在处理：",file_path)


statistics(text_path)


