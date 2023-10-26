import os
import model_L
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score, auc, precision_recall_curve, average_precision_score, cohen_kappa_score
import matplotlib

matplotlib.rc("font", family='SimHei')
matplotlib.rcParams['axes.unicode_minus'] = False

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import tensorboard



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


model = keras.models.load_model("Recognition\\datasets\\model\\cnn_model_2.h5")

y_pred = model.predict(X_test)


# 混淆矩阵
conf_matrix = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print("Confusion Matrix:")
print(conf_matrix)

# 分类报告
class_report = classification_report(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print("Classification Report:")
print(class_report)

# ROC 曲线和AUC
n_classes = y_test.shape[1]
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    
# 绘制 ROC 曲线
plt.figure(figsize=(8, 6))
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()

# 精确度-召回率曲线和AUC
precision = dict()
recall = dict()
pr_auc = dict()
for i in range(n_classes):
    precision[i], recall[i], _ = precision_recall_curve(y_test[:, i], y_pred[:, i])
    pr_auc[i] = auc(recall[i], precision[i])

# 绘制精确度-召回率曲线
plt.figure(figsize=(8, 6))
for i in range(n_classes):
    plt.plot(recall[i], precision[i], label=f'Class {i} (AUC = {pr_auc[i]:.2f})')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()

# Kappa 统计量
kappa = cohen_kappa_score(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print(f"Kappa Statistic: {kappa:.2f}")