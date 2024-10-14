## Obtaining the datasets

To train the model, you need the datasets. You can get them through one of the following methods:
1. You can **unzip** the files available in the `dataset` (current) directory (`setup` script should do that for you).
   > These files contain the datasets I've used during the learning process that are already hand-picked
   > and standardized for better results.
2. You can check `README.md` file to find out how to **download** the datasets separately. However, keep in mind that:
    - images downloaded from the original sources won't be standardized and hand-picked
    - if you don't want to modify the code in notebooks,
      you should replicate the following structure of subfolders within the `dataset` directory:
        - `Familyguy` - images from the _Cartoon Classification_ dataset
        - `VincentVanGogh` - images from the _Van Gogh Paintings_ dataset
        - `natural_images` - images from the _Natural Images_ dataset
          - `natural_images/mscoco` - images from the _mscoco_ dataset
3. You can obviously **study** the notebooks **yourself** and try to use **entirely different** datasets!

The proper structure of the `dataset` directory is **shown below** _(at the end of this file)_.

### How I've processed the datasets...
1. The following datasets have been **standardized** to 512x512 resolution:
   - `Familyguy`
   - `VincentVanGogh`
   - `natural_images/flower`
   As a result, some images might be cropped. **VincentVanGogh** has also lost its subfolder categories structure
   after standardization since preserving it wasn't crucial.
2. **natural_images** and **VincentVanGogh** datasets contain images from **different categories**,
   so you can choose the ones you think might bring the best results.
3. **Familyguy** requires **hand-picking** the most different images as there are a lot of similar ones. \
   I can recommend the following approach:
   - Use `dataset_cleaner.py` script to keep only every 20th file in the directory.
   - Hand-pick the most different images from the remaining ones.
4. It isn't a necessity but I've also hand-picked the best photos
   in **VincentVanGogh** dataset to increase the variation.

### Dataset structure
Here's how the final structure should look like:
```
dataset
├───Familyguy
├───natural_images
│   ├───car
│   ├───flower
│   ├───mscoco
│   └───person
└───VincentVanGogh
```
It may obviously vary after making some changes to the code.