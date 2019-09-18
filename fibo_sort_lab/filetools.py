import os
import shutil
import random
from contextlib import contextmanager


def write(file, num):
    num_bytes = int.to_bytes(num, 4, byteorder='little', signed=True)
    file.write(num_bytes)


def read(file):
    num_bytes = file.read(4)
    return int.from_bytes(num_bytes, byteorder='little', signed=True) if len(num_bytes) == 4 else None


def clear(*files):
    for file in files:
        file.seek(0)
        file.truncate()


def cutleft(file):
    fs, fp = 0, file.tell()
    end = file.seek(0, 2)
    size = end - fp
    file.seek(fp)

    while fp < end:
        file.seek(fp)
        byte = file.read(1)
        fp += 1
        file.seek(fs)
        file.write(byte)
        fs += 1

    file.seek(0)
    file.truncate(size)


with open('test.txt', 'r+') as f:
    f.seek(10)
    cutleft(f)


@contextmanager
def create_temp_files(directory: str, files_quantity: 'int > 0'):
    try:
        os.mkdir(directory)
        files = [open(f'{directory}/{i}.bin', 'wb') for i in range(files_quantity)]
        filenames = [f.name for f in files]
        for f in files:
            f.close()
        files = [open(fname, 'rb+') for fname in filenames]
        yield files
    finally:
        for f in files:
            f.close()
        shutil.rmtree(directory, ignore_errors=True)


def generate_test_file(file_title: str, num_quantity: 'int > 0'):
    with open(file_title + '.bin', 'wb') as f:
        num_count = 0
        while num_count < num_quantity:
            write(f, random.randint(0, 5000))
            num_count += 1
