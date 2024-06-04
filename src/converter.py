import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image

from generator import CycleGenerator, SRGenerator


def cycle_preprocess_image(img_name: str, reduce_colours: int = None):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if reduce_colours:  # reducing colours by applying LUT filter
        levels = reduce_colours
        lut_filter = np.zeros(256, dtype=np.uint8)
        step = 256 // levels
        for i in range(256):
            lut_filter[i] = (i // step) * step + step // 2
        img = cv2.LUT(img, lut_filter)

    img = np.array([img], dtype=np.float32) / 255  # converting to float32 and scaling between 0 and 1
    return next(iter(tf.data.Dataset.from_tensor_slices(img).batch(1)))


def convert(img_name: str, style: str):
    if style == "Vincent Van Gogh Art":
        convert_van_gogh(img_name)
    elif style == "Cartoon":
        convert_cartoon(img_name)
    else:
        raise Exception("No style conversion mode selected!")


def plot_and_save(img, conversion, img_name: str, tmp_path: str = "../tmp",
                  styled: bool = False, compare: bool = True, upscaled: bool = False):
    if compare:
        plt.figure(dpi=128, facecolor="#3b3b3b")
        plt.subplot(1, 2, 1)
        plt.imshow(img[0])
        plt.axis("off")
        plt.subplot(1, 2, 2)
        plt.imshow(conversion)
        plt.axis("off")
        plt.savefig(tmp_path + "/conversion.png", bbox_inches='tight', pad_inches=0)

    fig, ax = plt.subplots(figsize=(1, 1), dpi=512 if upscaled else 256)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.imshow(conversion)
    ax.axis("off")

    filename = img_name if styled else tmp_path + "/partial.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)


def initialize_style_gen(weights_path: str) -> CycleGenerator:
    style_generator = CycleGenerator().build()
    style_generator.load_weights(weights_path)
    return style_generator


def convert_van_gogh(img_name: str):
    van_gogh_generator = initialize_style_gen(weights_path="../models/van_gogh.weights.h5")
    img = cycle_preprocess_image(img_name)

    conversion = van_gogh_generator(img, training=False)[0].numpy()
    conversion = (conversion * 127.5 + 127.5).astype(np.uint8)
    plot_and_save(img, conversion, img_name, compare=False)


def convert_cartoon(img_name: str):
    cartoon_generator = initialize_style_gen(weights_path="../models/cartoon.weights.h5")
    img = cycle_preprocess_image(img_name, reduce_colours=8)

    conversion = cartoon_generator(img, training=False)[0].numpy()
    conversion = (conversion * 127.5 + 127.5).astype(np.uint8)
    plot_and_save(img, conversion, img_name, compare=False)


def sr_preprocess_image(styled_image: str):
    img = Image.open(styled_image).convert('RGB')
    return np.array([np.array(img)], dtype='float32') / 127.5 - 1


def initialize_srgan(weights_path: str = "../models/srgan.weights.h5") -> SRGenerator:
    sr_generator = SRGenerator().build()
    sr_generator.load_weights(weights_path)
    return sr_generator


def upscale(img_name: str, original_img_path: str, style_converted_img_path: str = "../tmp/partial.png"):
    generator = initialize_srgan()

    org = sr_preprocess_image(original_img_path)
    img = sr_preprocess_image(style_converted_img_path)

    pred = generator(img, training=False)

    org, pred = (org + 1) * 127.5, (pred + 1) * 127.5
    org, pred = np.array(org, dtype='uint8'), np.array(pred, dtype='uint8')
    plot_and_save(org, pred[0], img_name, styled=True, compare=True, upscaled=True)


def clean(tmp_path: str = "../tmp", keep_partial: bool = False, keep_converted_comparison: bool = False):
    if not keep_partial:
        os.remove(tmp_path + "/partial.png")
    if not keep_converted_comparison:
        os.remove(tmp_path + "/conversion.png")
