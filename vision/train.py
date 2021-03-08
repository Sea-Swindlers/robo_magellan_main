# For running inference on the TF-Hub module.
import tensorflow as tf

# For downloading the image.
import matplotlib.pyplot as plt

# For measuring the inference time.
import time

from nn_utils import load_img, draw_boxes, display_image

from networks import MoblenetV2SSD, LinearNetKeras


# The actual line
TRUE_W = 3.0
TRUE_B = 2.0

NUM_EXAMPLES = 1000

# A vector of random x values
x = tf.random.normal(shape=[NUM_EXAMPLES])

# Generate some noise
noise = tf.random.normal(shape=[NUM_EXAMPLES])

# Calculate y
y = x * TRUE_W + TRUE_B + noise

# Plot all the data
import matplotlib.pyplot as plt

plt.scatter(x, y, c="b")
plt.show()




keras_model = LinearNetKeras()

# compile sets the training paramaeters
keras_model.compile(
    # By default, fit() uses tf.function().  You can
    # turn that off for debugging, but it is on now.
    run_eagerly=False,

    # Using a built-in optimizer, configuring as an object
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),

    # Keras comes with built-in MSE error
    # However, you could use the loss function
    # defined above
    loss=tf.keras.losses.mean_squared_error,
)

print(x.shape[0])
keras_model.fit(x, y, epochs=10, batch_size=1000)



# Visualize how the trained model performs
plt.scatter(x, y, c="b")
plt.scatter(x, keras_model(x), c="r")
plt.show()

print("Current loss: %1.6f" % loss(model(x), y).numpy())







