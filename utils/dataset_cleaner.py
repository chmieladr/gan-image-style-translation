import os


def file_cleaner(directory: str):
    files = os.listdir(directory)
    for i, file in enumerate(files, start=1):
        if i % 20 != 0:
            os.remove(os.path.join(directory, file))


if __name__ == '__main__':
    dir_path = '../dataset/Familyguy'
    file_cleaner(dir_path)
