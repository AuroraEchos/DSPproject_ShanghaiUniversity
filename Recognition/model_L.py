from tensorflow import keras

def cnn_model(X_train, y_train):
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),      # 添加卷积层
        keras.layers.MaxPooling2D((2, 2)),                                                  # 添加最大池化层
        keras.layers.Conv2D(64, (3, 3), activation='relu'),                                 # 添加第二个卷积层
        keras.layers.MaxPooling2D((2, 2)),                                                  # 再次添加最大池化层
        keras.layers.Conv2D(128, (3, 3), activation='relu'),                                # 添加第三个卷积层
        keras.layers.MaxPooling2D((2, 2)),                                                  # 再次添加最大池化层
        keras.layers.Conv2D(128, (3, 3), activation='relu'),                                # 添加第四个卷积层
        keras.layers.MaxPooling2D((2, 2)),                                                  # 再次添加最大池化层

        keras.layers.Flatten(),

        keras.layers.Dense(512, activation='relu'),                                         # 添加全连接层
        keras.layers.Dropout(0.5),                                                          # 添加Dropout层以减少过拟合
        keras.layers.Dense(128, activation='relu'),                                         # 再添加一个全连接层
        keras.layers.Dense(5, activation='softmax')                                         # 输出层
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy']
                  )
    
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
    model.save("Recognition\\datasets\\model\\cnn_model_2.h5")

    return model
