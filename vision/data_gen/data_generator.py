
import os
import numpy as np
import PIL
from PIL import Image
import cv2
import matplotlib.pyplot as plt

'''
@David, may I interest you in dataclasses https://docs.python.org/3/library/dataclasses.html. 

>> from dataclasses import dataclass
>> from typing import Optional
>> 
>> @dataclass
>> class ImageSpec:
>>     base_image: Optional[str] = None
>>     cone_image: Optional[str] = None
>>     cone_center: [float, float] = [0.5, 0.5]
>>     cone_size: float = 1.0
>>     cone_angle: float = 0
>>
>> image_spec = ImageSpec('temp.png')
>> print(image_spec.base_image)
>> temp.png

Also I think I think yolo training takes in bounding boxes (tlbr or tlwh)
'''
class AdditionSpec:
    def __init__(self,
                    image_name: str,
                    center_position: [float, float] = [0.5, 0.5],
                    size: float = 0.25,
                    angle: float = 0,
                    recolor: [float, float, float] = [0, 0, 0],
                    needs_bounding_box: bool = True):
        self.image_name = image_name
        self.center_position = center_position
        self.size = size
        self.angle = angle
        self.recolor = recolor
        self.needs_bounding_box = needs_bounding_box


class ImageSpec:
    def __init__(self, 
                    base_image: str = None, 
                    additions: [AdditionSpec] = None,
                    recolor: [float, float, float] = [0, 0, 0]):
        """
        stores everything there is to know about a synthetic training image

        @param base_image: file name of the background image
        @param cone_image: file name of the cone image
        """
        self.base_image = base_image
        self.additions = additions
        self.recolor = recolor


class DataGenerator:

    def __init__(self, image_base_path, output_size = [512, 512]):
        self.image_base_path = image_base_path
        self.output_size = output_size


    def get(self, index: int) -> np.ndarray:
        pass

    
    def get_image_and_bounding_boxes(self, image_spec: ImageSpec):

        base_image = np.array(self.load_and_resize(image_spec.base_image, target_size=self.output_size))
        bounding_boxes = []
        for addition in image_spec.additions:
            base_image, next_bounding_box = self.place_addition(base_image, addition)

            if addition.needs_bounding_box:
                bounding_boxes.append(next_bounding_box)
        
        return base_image, bounding_boxes


    def load_and_resize(self, path, target_size=None, size_ratio=None) -> np.ndarray:
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
            return np.array(img_sized_one)

        else:
            img_sized_one = img.resize((int(target_size[0]), int(target_size[1])), resample = PIL.Image.BILINEAR)
            return np.array(img_sized_one)


    def place_addition(self, base_image: np.ndarray, addition: AdditionSpec) -> (np.ndarray, (int, int, int, int)):
        """
        bounding box format is [ymin, xmin, ymax, xmax]
        """
        #TODO: rest of image augmentation
        addition_img = self.load_and_resize(addition.image_name, target_size = self.output_size, size_ratio = addition.size)

        cone_image_no_transparency = addition_img[:, :, 0:3]
        transparency_mask = addition_img[:, :, 3] != 0

        # paste the cone onto the base image
        top_corner_y = int(base_image.shape[0] * addition.center_position[0]) - (addition_img.shape[0] // 2)
        top_corner_x = int(base_image.shape[1] * addition.center_position[1]) - (addition_img.shape[1] // 2)
        bottom_corner_y = top_corner_y + addition_img.shape[0]
        bottom_corner_x = top_corner_x + addition_img.shape[1]

        base_image[top_corner_y : bottom_corner_y, top_corner_x : bottom_corner_x] = base_image[top_corner_y : bottom_corner_y, top_corner_x : bottom_corner_x] * (1 - transparency_mask[:, :, np.newaxis])
        base_image[top_corner_y : bottom_corner_y, top_corner_x : bottom_corner_x] += cone_image_no_transparency * transparency_mask[:, :, np.newaxis]

        return base_image, [top_corner_y, top_corner_x, bottom_corner_y, bottom_corner_x]
