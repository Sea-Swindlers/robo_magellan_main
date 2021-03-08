"""
This is a script that crops all training images based off of alpha channel
So for every image in the training data folder, if there is a row of transparent pixels at the edge of an image, it is cut away
"""

import os
import numpy as np
import PIL
from PIL import Image
import itertools
import functools
from matplotlib import pyplot as plt


# from https://codereview.stackexchange.com/questions/153029/recursively-list-files-within-a-directory
def files_within(directory_path):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for file_name in filenames:
            if file_name.lower().endswith("jpg") or file_name.lower().endswith("png"):
                relative_path = os.path.join(dirpath[len(directory_path): ], file_name)
                yield relative_path if relative_path[0] != "/" else relative_path[1:]



def trim_bottom(img: np.ndarray) -> np.ndarray:
    alpha_values = img[:, :, 3].max(axis=1)
    greatest_line_with_content = functools.reduce(lambda x, y: x if y[1] == 0 else y, enumerate(alpha_values), [-1, 0])[0]
    return img[0:greatest_line_with_content, :, :]
    

def rotate_image(img: np.ndarray):
    return img.transpose((1, 0, 2))[::-1, :, :]
    # return img.transpose((1, 0, 2))


def main(image_base_path="/home/david/robo_magellan_main/vision/data"):
    for image_path in files_within(image_base_path):
        if image_path[-4:] != ".png":
            continue
        try:
            img = np.array(Image.open(os.path.join(image_base_path, image_path)))
        except e:
            print(e)
            continue
        if img.shape[2] == 3:
            continue
        for i in range(4):
            trimmed = trim_bottom(img)
            img = rotate_image(trimmed)
        
        # plt.imshow(img)
        # plt.show()
        modified = Image.fromarray(img)
        modified.save(os.path.join(image_base_path, image_path))


if __name__ == "__main__":
    main()
