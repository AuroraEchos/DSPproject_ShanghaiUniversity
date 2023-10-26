import os
import time
import warnings
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from scipy import signal
from tensorflow import keras
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings('ignore')


def newaudio_predict(new_img_path):
    #print("开始准备预测")
    #print("请稍等......")
    time.sleep(1)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    label_path = os.path.join(desktop_path, "Dsp", "Recognition", "datasets", "label" ,"labels.csv")
    labels_df = pd.read_csv(label_path)
    file_names = labels_df['Filename'].values
    labels = labels_df['Label'].values

    try:
        npy_path = os.path.join(desktop_path, "Dsp", "Recognition", "datasets", "datanpy" ,"img_data.npy")
        data = np.load(npy_path)
    except FileNotFoundError:
        print("未找到保存的频谱图数据，正在重新加载...")
        data = []
        for file_name in file_names:
            img_path = os.path.join("Recognition\\datasets\\img\\",file_name)
            img = keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
            img_array = keras.preprocessing.image.img_to_array(img)
            data.append(img_array)
            print("正在处理：",file_name)
        data = np.array(data)
        np.save("Recognition\\datasets\\datanpy\\img_data.npy", data)

    encoder = LabelEncoder()
    labels_encoded = encoder.fit_transform(labels)
    labels_encoded = tf.keras.utils.to_categorical(labels_encoded)

    h5_path = os.path.join(desktop_path, "Dsp", "Recognition", "datasets", "model" ,"cnn_model_2.h5")
    loaded_model = keras.models.load_model(h5_path)

    new_img_path = new_img_path
    new_img = keras.preprocessing.image.load_img(new_img_path, target_size=(256, 256))
    new_img_array = keras.preprocessing.image.img_to_array(new_img)
    new_img_array = np.expand_dims(new_img_array, axis=0)
    predictions = loaded_model.predict(new_img_array,verbose=0)
    predicted_label = encoder.inverse_transform([np.argmax(predictions)])[0]

    if predicted_label == "Wenhao":
        #print(f"预测结果: 刘文豪")
        result = '预测结果: 刘文豪'
    elif predicted_label == "Hui":
        #print(f"预测结果: 赵慧")
        result = '预测结果: 赵慧'
    elif predicted_label == "Jiajia":
        #print(f"预测结果: 胡佳佳")
        result = '预测结果: 胡佳佳'
    elif predicted_label == "Junjia":
        #print(f"预测结果: 马俊佳")
        result = '预测结果: 马俊佳'
    elif predicted_label == "Zhenjie":
        #print(f"预测结果: 马振杰")
        result = '预测结果: 马振杰'

    return result

def channel_process(new_img_save):
    #print("开始转换通道")
    time.sleep(1)
    image = Image.open(new_img_save)
    image = image.convert('RGB') 
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    img_path = os.path.join(desktop_path, "Dsp", "Recognition", "datasets", "predict" ,"new_img.png")
    save_path = img_path
    image.save(save_path)
    #print("通道转换完成")
    #print("-"*30)
    newaudio_predict(new_img_path=new_img_save)


def newaudio_process(new_audio_path):
    #print("开始进行音频处理")
    #print("请稍等......")
    #print("-"*30)
    time.sleep(1)
    #print("开始提取频谱图")
    time.sleep(1)
    sample_rate, audio_data = wav.read(new_audio_path)
    f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate, nperseg=512, noverlap=256, nfft=1024)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    img_path = os.path.join(desktop_path, "Dsp", "Recognition", "datasets", "predict" ,"new_img.png")
    new_img_save = img_path
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    plt.axis('off') 
    plt.savefig(new_img_save, bbox_inches='tight', pad_inches=0, dpi=256, format='png', transparent=False)
    plt.close()
    #print("频谱图提取完成")
    #print("-"*30)
    time.sleep(1)
    channel_process(new_img_save=new_img_save)

    # 调用预测函数并返回预测结果
    predicted_name = newaudio_predict(new_img_path=new_img_save)

    return predicted_name

""" 
new_audio_path = "C:\\Users\\Administrator\\Desktop\\testaudio\\Jiajia\\7.wav"
print(newaudio_process(new_audio_path)) """