import matplotlib.pyplot as plt
import numpy as np
import PIL
import data_generator as datagen


def main():
    image_spec = datagen.ImageSpec(base_image = "landscapes/landscape_1.jpg",
                                    cone_image = "cones/cone_1.png",
                                    cone_size = 0.15,
                                    cone_center = (0.7, 0.7))

    data_generator = datagen.DataGenerator(image_base_path="/home/david/robo_magellan_main/vision/data")

    output = data_generator.place_cone(image_spec)

    plt.imshow(output)
    # plt.savefig("output.png")
    plt.show()


if __name__ == "__main__":
    main()
