# Python program that takes a directory with images and crops them to a square shape,
# then resizes them to 512x512 pixels using bicubic resampling.

import os
from PIL import Image


def process_images(input_directory: str, output_directory: str):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, filename)
                with Image.open(img_path) as img:
                    width, height = img.size
                    x = min(width, height)

                    left = (width - x) // 2
                    top = (height - x) // 2
                    right = left + x
                    bottom = top + x

                    img_final = img.crop((left, top, right, bottom)).resize((512, 512),
                                                                            resample=Image.Resampling.BICUBIC)
                    output_path = os.path.join(output_directory, filename)
                    img_final.save(output_path)


directories = ['../dataset/natural_images/flower',
               '../dataset/VincentVanGogh',
               '../dataset/Familyguy',
               '../tmp',
               ]

if __name__ == '__main__':
    input_dir = directories[3]
    output_dir = input_dir + '_standardized'
    process_images(input_dir, output_dir)
