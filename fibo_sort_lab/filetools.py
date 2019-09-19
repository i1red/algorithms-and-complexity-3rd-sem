import os
import shutil
import random
import struct
from contextlib import contextmanager, suppress
from array import array


def write(file, num):
    file.write(struct.pack('i', num))


def read(file):
    num_bytes = file.read(4)
    return struct.unpack('i', num_bytes)[0] if len(num_bytes) == 4 else None


def read_chunk(file, size):
    chunk = array('i', [])
    with suppress(EOFError):
        chunk.fromfile(file, size)
    return chunk


def clear(*files):
    for file in files:
        file.seek(0)
        file.truncate()


def cutleft(*files):
    for file in files:
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


def write_array():
    pass


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
        for i in range(num_quantity):
            write(f, random.randint(0, 5000))
