import matplotlib.pyplot as plt
import numpy as np
import PIL
import data_generator as datagen
import os
import pathlib


def draw_bounding_box(img: np.ndarray, corners, color = np.array([255, 0, 0])):
    img[corners[0] : corners[2], corners[1]] = color
    img[corners[0] : corners[2], corners[3]] = color
    img[corners[0], corners[1] : corners[3]] = color
    img[corners[2], corners[1] : corners[3]] = color


def main():
    distraction_spec = datagen.AdditionSpec(image_name="decoys/Fire_hydrant.png", needs_bounding_box=False, center_position=[0.3, 0.7])
    cone_spec = datagen.AdditionSpec(image_name="cones/cone_1.png", needs_bounding_box=True, center_position=[0.7, 0.3])
    image_spec = datagen.ImageSpec(base_image = "landscapes/landscape_1.jpg",
                                    additions=[cone_spec, distraction_spec])

    base_path = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), "data")

    data_generator = datagen.DataGenerator(base_path)
    # data_generator = datagen.DataGenerator("/home/david/robo_magellan_main/vision/data")

    output = data_generator.get_image_and_bounding_boxes(image_spec)

    print(output[1])

    draw_bounding_box(output[0], output[1][0])

    plt.imshow(output[0])
    plt.savefig("output.png")
    # plt.show()


if __name__ == "__main__":
    main()
