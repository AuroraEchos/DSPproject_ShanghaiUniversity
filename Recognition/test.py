import os
import model_L
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


labels_df = pd.read_csv("datasets\\label\\labels.csv")

file_names = labels_df['Filename'].values
labels = labels_df['Label'].values


try:
    data = np.load("datasets\\datanpy\\img_data.npy")
except FileNotFoundError:
    print("未找到保存的频谱图数据，正在重新加载...")
    data = []
    for file_name in file_names:
        img_path = os.path.join("datasets\\img\\",file_name)
        img = keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array)
        print("正在处理：",file_name)
    data = np.array(data)
    np.save("datasets\\datanpy\\img_data.npy", data)


encoder = LabelEncoder()
labels_encoded = encoder.fit_transform(labels)
labels_encoded = tf.keras.utils.to_categorical(labels_encoded)


loaded_model = keras.models.load_model("datasets\\model\\cnn_model.h5")

new_img_path = "datasets\\img\\Wenhao_Liu122.png"
new_img = keras.preprocessing.image.load_img(new_img_path, target_size=(256, 256))
new_img_array = keras.preprocessing.image.img_to_array(new_img)
new_img_array = np.expand_dims(new_img_array, axis=0)
predictions = loaded_model.predict(new_img_array,verbose=0)
predicted_label = encoder.inverse_transform([np.argmax(predictions)])[0]
print(f"Predicted label: {predicted_label}")