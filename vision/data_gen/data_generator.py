
import os
import numpy as np
import PIL
from PIL import Image
import cv2
import matplotlib.pyplot as plt


class ImageSpec:
    def __init__(self, 
                    base_image: str = None, 
                    cone_image: str = None, 
                    cone_center: [float, float] = [0.5, 0.5], 
                    cone_size: float = 0.1, 
                    cone_angle: float = 0, 
                    white_is_transparent: bool = True):
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
        self.white_is_transparent = white_is_transparent


class DataGenerator:

    def __init__(self, image_base_path, output_size = [512, 512]):
        self.image_base_path = image_base_path
        self.output_size = output_size


    def get(self, index: int) -> np.ndarray:
        pass

    
    def place_cone(self, image_spec: ImageSpec) -> np.ndarray:

        def load_and_resize(path, target_size=None, size_ratio=None, remove_background=False):
            if target_size is None and size_ratio is None:
                print("ERROR fix your code (load_and_resize called without target_size or size_ratio set")
                # TODO: write a real error message
                return
            
            img = Image.open(os.path.join(self.image_base_path, path))
            if size_ratio is not None:
                max_dim = max(img.size)
                new_size_0 = int(target_size[0] * size_ratio * img.size[0] / max_dim)
                new_size_1 = int(target_size[1] * size_ratio * img.size[1] / max_dim)
                img_sized_one = img.resize((new_size_0, new_size_1), resample = PIL.Image.BILINEAR)
                return img_sized_one

            else:
                img_sized_one = img.resize((int(target_size[0]), int(target_size[1])), resample = PIL.Image.BILINEAR)
                return img_sized_one


        base_image = load_and_resize(image_spec.base_image, target_size = self.output_size)
        cone_image = load_and_resize(image_spec.cone_image, target_size = self.output_size, size_ratio = image_spec.cone_size)

        base_image = np.array(base_image)
        cone_image = np.array(cone_image)

        cone_image_no_transparency = cone_image[:, :, 0:3]
        transparency_mask = cone_image[:, :, 3] != 0

        # plt.imshow(cone_image_no_transparency)
        # plt.show()

        # paste the cone onto the base image
        size_1, size_2, _ = base_image.shape
        cone_size_1, cone_size_2, _ = cone_image.shape
        cone_top_corner_1 = int(size_1 * image_spec.cone_center[0]) - (cone_size_1//2)
        cone_top_corner_2 = int(size_2 * image_spec.cone_center[1]) - (cone_size_2//2)

        base_image[cone_top_corner_1 : cone_top_corner_1 + cone_size_1, cone_top_corner_2 : cone_top_corner_2 + cone_size_2] = base_image[cone_top_corner_1 : cone_top_corner_1 + cone_size_1, cone_top_corner_2 : cone_top_corner_2 + cone_size_2] * (1 - transparency_mask[:, :, np.newaxis])

        base_image[cone_top_corner_1 : cone_top_corner_1 + cone_size_1, cone_top_corner_2 : cone_top_corner_2 + cone_size_2] += cone_image_no_transparency * transparency_mask[:, :, np.newaxis]

        return base_image

