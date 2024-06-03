## Obtaining the model files (weights)

To use the program, you need to download the model files. There are two possible approaches:
1. You can download the model files from the following link and place them in the `models` directory. \
https://drive.google.com/drive/folders/1BJkz7L-KXaFDawDjntKGmJG5qqrEUOse?usp=drive_link
2. Train the models yourself using the _Jupyter notebooks_ available in `notebooks` directory.
If you don't change the save directory, they will be saved in the `models` folder.

Make sure that the names of models are as follows (otherwise the main program won't be able to find them):

| Model                                                                  | Filename               |
|------------------------------------------------------------------------|------------------------|
| **CycleGAN** responsible for **Van Gogh Art** style conversion         | `van_gogh.weights.h5`  |
| **CycleGAN** responsible for **Cartoon** style conversion              | `cartoon.weights.h5`   | 
| **PatchGAN** responsible for **upscaling** output image to **512x512** | `patch_gan.weights.h5` |

> **Note!** The files above contain only the **generator's** weights as the entire model isn't necessary for the main app.
> However, inside of _Google Drive_ provided above you can also find the whole model files in case you want to use them for further research.