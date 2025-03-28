# Ganics - GAN-based image style translation app
Python application that translates the style of given input image to one of the following:
- **Vincent Van Gogh art**
- **Cartoon**

The style-translated image is produced in _256x256_ resolution, then upscaled to _512x512_ using another network.

> **Note!** The output will always be **512x512 .png image**, no matter what the initial image resolution and format were.

## Environment setup
In order to run the application from **source code**, you can use `conda` to create the proper environment. You can also utilise `venv` for this purpose. \
For this purpose, feel free to use one of the available `setup` scripts or have a look at them and replicate a similar environment on your own!

#### Linux
```shell
chmod +x setup.sh
./setup.sh         # configures the environment and extracts the datasets
./setup.sh test    # does the same and additionally extracts the images for testing
```

#### Windows
```shell
.\setup.ps1        # configures the environment and extracts the datasets
.\setup.ps1 test   # does the same and additionally extracts the images for testing
```
After creating the environment, you can launch the application using this command:
```shell
python src/main.py
```
The application's GUI should now show up. If it doesn't, you might have to install `tkinter` package.

> **Note!** This app uses Tensorflow **2.17** which is not supported on **Windows** operating system anymore. \
> You can try installing **Tensorflow 2.10** to go around this but I don't guarantee everything will work properly.

## Model
This project uses **CycleGANs** to translate the style of input image.
Then uses **SRGAN** with **PatchGAN** discriminator to upscale the output to higher resolution. \
All models are initialized using tensorflow's `tf.keras` API. \
Models can be either trained by yourself using _Jupyter Notebook_ files available in `notebooks` subfolder
or downloaded using the link available in `models/how_to_get_models.md` file.

## Documentation
You can find more **in-depth** documentation of this project in the `docs` subfolder.
It contains the documentation of the entire project, including the description of
the dataset, model, and the application itself.

## Project structure
Context of each subfolder has been described below:
- `dataset` - contains all the datasets used for **training the models** (all datasets from _Kaggle_ - sources available below)
  - `Familyguy` (coming from _Cartoon Classification_ dataset) - frames taken from the _Family Guy_ series used for training the cartoon style
  - `natural_images` - images of different **natural scenes**
  - `VincentVanGogh` - images of **Vincent Van Gogh** art
  - `info.md` - instructions on how to obtain datasets that I've used during learning process
    - **_You should check this file before trying to launch Jupyter notebooks!_**
- `docs` - entire **documentation** of the project
  - `en` - _English_ version
  - `pl` - _Polish_ version
  - `imgs` - contains all the graphics used in the documentation
  - `.tex` files - used for generating the documentation in _LaTeX_
  - `.pdf` files - actual documentation in _PDF_ format
- `models` - **trained models** used for converting the image 
  - `how_to_get_models.md` - instructions on how to obtain necessary files with models
    - **_It is highly recommended to check it before trying to launch the application!_**
- `notebooks` - _Jupyter Notebooks_ used for training the models
- `src` - actual **code** of the **application**
  - `converter.py` - functions that **preprocess** the input image and **convert** it to the **desired style**
  - `custom_layers.py` - custom _tf.keras.Layer_ layers used in the models
  - `generator.py` - initialization of **generative models**
  - `gui.py` - responsible for building an entire **tkinter GUI**
  - `main.py` - **main** script that launches the **application**
  - `resample.py` - creating **layers** responsible for either **reducing** or **increasing** the spatial dimensions of the input image
- `tmp` - directory made for **temporary files**
  - `test_imgs.zip` contains some additional example images for testing purposes _(not used in the training process)_ 
- `utils` - contains **other scripts** used for the project that aren't a part of main application
  - `dataset_cleaner.py` - script that can be used to keep **only every 20th file** in given directory
    - used for _Familyguy_ dataset as it contained a lot of similar images (followed by later hand-picking the most different ones)
  - `standarize_imgs.py` - script used for **standardizing images** into 512x512 format
    - used to standardize images from _Familyguy_ and _VincentVanGogh_ datasets

## Sources
This project wouldn't exist without the sources below. You can check them out for more information.

### Datasets
- **Familyguy** (from _Cartoon Classification_ dataset below)
  - https://www.kaggle.com/datasets/volkandl/cartoon-classification
- **mscoco** (`natural_images/mscoco`)
  - https://www.kaggle.com/datasets/aftaab/mscoco
- **natural_images**
  - https://www.kaggle.com/datasets/prasunroy/natural-images/data
- **VincentVanGogh**
  - https://www.kaggle.com/datasets/ipythonx/van-gogh-paintings

### Generative Adversarial Networks
- **CycleGAN** - Style transferring
  - https://www.kaggle.com/code/mehmetlaudatekman/style-transfering-with-van-gogh-cyclegan
  - https://junyanz.github.io/CycleGAN/ 
- **GAN-based Image upscaling**
  - https://www.kaggle.com/code/amanrajput27/gan-based-image-upscaling
  - https://www.tensorflow.org/tutorials/generative/pix2pix
  - https://arxiv.org/abs/1609.04802

### Other
- **tkinter** - GUI rendering
  - https://docs.python.org/3/library/tkinter.html
