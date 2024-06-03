import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from custom_layers import InstanceNormalization


def downsample(filters: int, size: int, instance_norm: bool = True):
    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = keras.Sequential()
    result.add(layers.Conv2D(filters, size, strides=2, padding="same", kernel_initializer=initializer, use_bias=False))
    if instance_norm:
        result.add(InstanceNormalization(gamma_initializer=gamma_init))
    result.add(layers.LeakyReLU())
    return result


def upsample(filters: int, size: int, dropout: bool = False):
    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = keras.Sequential()
    result.add(layers.Conv2DTranspose(filters, size, strides=2, padding="same",
                                      kernel_initializer=initializer, use_bias=False))
    result.add(InstanceNormalization(gamma_initializer=gamma_init))
    if dropout:
        result.add(layers.Dropout(0.5))
    result.add(layers.ReLU())
    return result
