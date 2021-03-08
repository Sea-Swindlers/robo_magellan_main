import tensorflow as tf
from PIL import Image
import numpy as np

import pdb


raw_image = Image.open("output.png").resize((224, 224))
x = np.array(raw_image)[np.newaxis, :, :, 0:3]

print(f"loaded image with shape {x.shape}")


preprocess_x = tf.keras.applications.mobilenet_v2.preprocess_input(
    x, data_format=None
)


model = tf.keras.applications.MobileNetV2(
    input_shape=None, alpha=1.0, include_top=True, weights='imagenet',
    input_tensor=None, pooling=None, classes=1000,
    classifier_activation='softmax'
)


pdb.set_trace()

