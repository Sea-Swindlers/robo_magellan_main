
import os
import numpy as np
import PIL
from PIL import Image
import cv2


class ImageSpec:
    def __init__(self, base_image: str = None, cone_image: str = None, cone_center: [float, float] = [0.5, 0.5], cone_size: float = 1.0, cone_angle: float = 0):
        """
        stores everything there is to know about a synthetic training image

        @param base_image: file name of the background image
        @param cone_image: file name of the cone image
        """
        self.base_image = base_image
        self.cone_image = cone_image
        self.cone_center = cone_center
        self.cone_size = cone_size
        self.cone_angle = cone_angle

class DataGenerator:

    def __init__(self, image_base_path, output_size = [512, 512]):
        self.image_base_path = image_base_path
        self.output_size = output_size

    def get(self, index: int) -> np.ndarray:
        pass

    
    def place_cone(self, image_spec: ImageSpec) -> np.ndarray:

        def load_and_resize(path, size_ratio=None):
            img = Image.open(os.path.join(self.image_base_path, path))
            if size_ratio is None:
                img = img.resize(self.output_size, resample = PIL.Image.BILINEAR)
            else:
                max_dim = max(img.size)
                img_sized_one = img.resize((self.output_size * img.size[0] / max_dim, self.output_size * img.size[1] / max_dim), resample = PIL.Image.BILINEAR)
            return img

        base_image = load_and_resize(image_spec.base_image, self.output_size)
        cone_image = load_and_resize(image_spec.cone_image, [self.output_size[0] * image_spec.)

        base_image = base_image.resize(self.output_size, resample = PIL.Image.BILINEAR)



