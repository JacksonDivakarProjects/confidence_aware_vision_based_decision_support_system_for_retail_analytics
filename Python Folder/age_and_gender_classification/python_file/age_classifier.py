import cv2
import numpy as np
import tensorflow as tf

class AgeClassifier:
    def __init__(self):
        self.class_indices = {
            0: '25-30',
            1: '42-48',
            2: '6-20',
            3: '60-98'
        }
        self.model = None

    def load_model(self, weights_path):
        inputs = tf.keras.layers.Input(shape=(200, 200, 3))

        x = tf.keras.layers.Conv2D(32, 3, strides=2, padding='same')(inputs)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)

        def residual(x, filters):
            shortcut = x
            if x.shape[-1] != filters:
                shortcut = tf.keras.layers.Conv2D(filters, 1, padding='same')(shortcut)
                shortcut = tf.keras.layers.BatchNormalization()(shortcut)

            x = tf.keras.layers.Conv2D(filters, 3, padding='same')(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.ReLU()(x)

            x = tf.keras.layers.Conv2D(filters, 3, padding='same')(x)
            x = tf.keras.layers.BatchNormalization()(x)

            return tf.keras.layers.ReLU()(tf.keras.layers.Add()([x, shortcut]))

        x = residual(x, 32)
        x = residual(x, 64)
        x = residual(x, 128)

        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        outputs = tf.keras.layers.Dense(4, activation='softmax')(x)

        self.model = tf.keras.Model(inputs, outputs)
        self.model.load_weights(weights_path)

    def predict(self, image):
        image = cv2.resize(image, (200, 200))
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)

        preds = self.model.predict(image, verbose=0)[0]
        idx = np.argmax(preds)

        return self.class_indices[idx], preds[idx] * 100
