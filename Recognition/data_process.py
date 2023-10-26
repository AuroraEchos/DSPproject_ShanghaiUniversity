import os
import numpy as np
import pandas as pd
from tensorflow import keras



def data_process(labels_path):
    labels_df = pd.read_csv(labels_path)
    file_names = labels_df['Filename'].values

    data = []
    for file_name in file_names:
        img_path = os.path.join("Recognition\\datasets\\img\\",file_name)
        img = keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array)
        print("正在处理：",file_name)
    data = np.array(data)
    np.save("Recognition\\datasets\\datanpy\\img_data.npy", data)

labels_path = "Recognition\\datasets\\label\\labels.csv"
data_process(labels_path)