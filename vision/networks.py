import tensorflow as tf
import tensorflow_hub as hub


class MoblenetV2SSD:
    def __init__(self):
        # module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
        module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"

        self.detector = hub.load(module_handle).signatures['default']

    def eval(self, img):
        converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
        return self.detector(converted_img)



class LinearNetKeras(tf.keras.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the weights to `5.0` and the bias to `0.0`
        # In practice, these should be randomly initialized
        self.w = tf.Variable(5.0)
        self.b = tf.Variable(0.0)

    def __call__(self, x, **kwargs):
        return self.w * x + self.b





