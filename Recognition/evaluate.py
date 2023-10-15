import os
import model_L
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, f1_score,average_precision_score
import matplotlib

matplotlib.rc("font", family='SimHei')
matplotlib.rcParams['axes.unicode_minus'] = False

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import tensorboard



labels_df = pd.read_csv("datasets\\label\\labels.csv")

file_names = labels_df['Filename'].values
labels = labels_df['Label'].values


try:
    data = np.load("datasets\\datanpy\\img_data.npy")
    print("已成功加载保存的频谱图数据")
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

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    data, 
    labels_encoded, 
    test_size=0.3, 
    random_state=42,
    shuffle=True
    )


loaded_model = keras.models.load_model("datasets\\model\\cnn_model.h5")

y_pred = loaded_model.predict(X_test)


# 计算每个标签的 ROC AUC 和平均精确度
roc_auc_scores = []
average_precision_scores = []

for i in range(y_test.shape[1]):
    fpr, tpr, _ = roc_curve(y_test[:, i], y_pred[:, i])
    roc_auc = roc_auc_score(y_test[:, i], y_pred[:, i])
    average_precision = average_precision_score(y_test[:, i], y_pred[:, i])

    # 绘制 ROC 曲线
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC 曲线 (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('假正例率 (FPR)')
    plt.ylabel('真正例率 (TPR)')
    plt.legend(loc='lower right')
    plt.title(f'ROC 曲线 - 标签 {i}')
    plt.show()

    # 绘制精确度-召回率曲线
    precision, recall, _ = precision_recall_curve(y_test[:, i], y_pred[:, i])
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2, label='精确度-召回率曲线')
    plt.xlabel('召回率 (Recall)')
    plt.ylabel('精确度 (Precision)')
    plt.legend(loc='lower left')
    plt.title(f'精确度-召回率曲线 - 标签 {i}')
    plt.show()

    roc_auc_scores.append(roc_auc)
    average_precision_scores.append(average_precision)

# 输出每个标签的 ROC AUC 和平均精确度
for i in range(len(roc_auc_scores)):
    print(f"标签 {i} 的ROC AUC: {roc_auc_scores[i]}")
    print(f"标签 {i} 的平均精确度: {average_precision_scores[i]}")