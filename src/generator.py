import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from resample import downsample, upsample


output_channels = len(["Red", "Green", "Blue"])  # RGB


class Generator:
    def __init__(self, strides: int = 2):
        self.initializer = tf.random_normal_initializer(0., 0.02)
        self.strides = strides
        self.inputs = layers.Input([256, 256, 3])
        self.outputs = None
        self.model = None
        self.down_stack, self.up_stack = None, None

    def __call__(self, inputs, training: bool = True):
        if not self.model:
            self.build()
        return self.model(inputs, training=training)

    def build(self) -> keras.Model:
        last_layer = layers.Conv2DTranspose(output_channels, 4,
                                            strides=self.strides,
                                            padding='same',
                                            kernel_initializer=self.initializer,
                                            activation='tanh')

        x = self.inputs
        skips = []
        for down in self.down_stack:
            x = down(x)
            skips.append(x)
        skips = reversed(skips[:-1])

        for up, skip in zip(self.up_stack, skips):
            x = up(x)
            x = layers.Concatenate()([x, skip])
        self.outputs = last_layer(x)
        self.model = keras.Model(inputs=self.inputs, outputs=self.outputs)
        return self.model


class CycleGenerator(Generator):
    def __init__(self, strides: int = 2):
        super(CycleGenerator, self).__init__(strides=strides)
        self.prepare_stacks()

    def prepare_stacks(self):
        self.down_stack = [downsample(64, 4),   # 128x128x64
                           downsample(128, 4),  # 64x64x128
                           downsample(256, 4),  # 32x32x256
                           downsample(512, 4),  # 16x16x512
                           downsample(512, 4),  # 8x8x512
                           downsample(512, 4),  # 4x4x512
                           downsample(512, 4),  # 2x2x512
                           downsample(512, 4),  # 1x1x512
                           ]
        self.up_stack = [upsample(512, 4, dropout=True),  # 2x2
                         upsample(512, 4, dropout=True),  # 4x4
                         upsample(512, 4),                # 8x8
                         upsample(256, 4),                # 16x16
                         upsample(128, 4),                # 32x32
                         upsample(64, 4),                 # 64x64
                         upsample(32, 4),                 # 128x128
                         ]


class PatchGenerator(Generator):
    def __init__(self, strides: int = 4):
        super(PatchGenerator, self).__init__(strides=strides)
        self.prepare_stacks()

    def prepare_stacks(self):
        # format: (bs = batch size, width, height, filters)
        # each downsampling reduces size by 2 because of stride = 2,
        self.down_stack = [
            downsample(32, 4, instance_norm=False),  # (bs, 128, 128, 32)
            downsample(64, 4),  # (bs, 64, 64, 64)
            downsample(128, 4),  # (bs, 32, 32, 128)
            downsample(256, 4),  # (bs, 16, 16, 256)
            downsample(512, 4),  # (bs, 8, 8, 512)
            downsample(512, 4),  # (bs, 4, 4, 512)
            downsample(512, 4),  # (bs, 2, 2, 512)
            downsample(512, 4),  # (bs, 1, 1, 512)
        ]
        self.up_stack = [
            upsample(512, 4, dropout=True),  # (bs, 2, 2, 1024)
            upsample(512, 4, dropout=True),  # (bs, 4, 4, 1024)
            upsample(512, 4, dropout=True),  # (bs, 8, 8, 1024)
            upsample(512, 4),  # (bs, 16, 16, 1024)
            upsample(256, 4),  # (bs, 32, 32, 512)
            upsample(128, 4),  # (bs, 64, 64, 256)
            upsample(64, 4),  # (bs, 128, 128, 128)
        ]
