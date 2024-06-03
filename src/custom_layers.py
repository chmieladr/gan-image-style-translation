import tensorflow as tf
from tensorflow.keras import layers


class InstanceNormalization(layers.Layer):
    def __init__(self, epsilon: float = 1e-5, gamma_initializer="ones", beta_initializer="zeros", **kwargs):
        super(InstanceNormalization, self).__init__(**kwargs)
        self.beta, self.gamma = None, None
        self.epsilon = epsilon
        self.gamma_initializer = gamma_initializer
        self.beta_initializer = beta_initializer

    def build(self, input_shape):
        self.gamma = self.add_weight(
            shape=(input_shape[-1],),
            initializer=self.gamma_initializer,
            trainable=True,
            name="gamma"
        )
        self.beta = self.add_weight(
            shape=(input_shape[-1],),
            initializer=self.beta_initializer,
            trainable=True,
            name="beta"
        )
        super(InstanceNormalization, self).build(input_shape)

    def call(self, inputs):
        mean, variance = tf.nn.moments(inputs, axes=[1, 2], keepdims=True)
        normalized = (inputs - mean) / tf.sqrt(variance + self.epsilon)
        return self.gamma * normalized + self.beta

    def get_config(self) -> dict:
        config = super(InstanceNormalization, self).get_config()
        config.update({"epsilon": self.epsilon})
        return config


class ResizeLayer(layers.Layer):
    def __init__(self, target_size, method='bicubic', **kwargs):
        super(ResizeLayer, self).__init__(**kwargs)
        self.target_size = target_size
        self.method = method

    def call(self, inputs):
        return tf.image.resize(inputs, self.target_size, method=self.method)
