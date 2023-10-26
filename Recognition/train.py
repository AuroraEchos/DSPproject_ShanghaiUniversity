import os
import model_L
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


#import tensorboard


labels_df = pd.read_csv("Recognition\\datasets\\label\\labels.csv")

file_names = labels_df['Filename'].values
labels = labels_df['Label'].values


try:
    data = np.load("Recognition\\datasets\\datanpy\\img_data.npy")
    print("已成功加载保存的频谱图数据")
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

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    data, 
    labels_encoded, 
    test_size=0.2, 
    random_state=42,
    shuffle=True
    )

# 训练模型
#tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="Recognition\\logs")

model = model_L.cnn_model(X_train,y_train)

# 在测试集上评估模型
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc}")

