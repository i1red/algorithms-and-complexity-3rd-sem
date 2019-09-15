import fibo_sort_lab.filetools as ftools
import uuid
import os


def divide(chunks_quantity, files_quantity):
    distribution = [0 for i in range(files_quantity)]
    tmp = list(distribution)
    distribution[0] = 1

    while sum(distribution) < chunks_quantity:
        max_val = max(distribution)
        index = distribution.index(max_val)
        for i in range(files_quantity):
            tmp[i] = 0 if i == index else tmp[i] + max_val
        distribution = list(tmp)

    return distribution


def fibo_sort(filename: str, chunk_size: 'int > 0', files_quantity: 'int > 2'):
    temp_files_dir = str(uuid.uuid4().hex)
    chunks_quantity = os.path.getsize(filename) // 4
    distribution = divide(chunks_quantity, files_quantity)
    with ftools.create_temp_files(temp_files_dir, files_quantity) as files:
        for f in files:
            print(f)


fibo_sort('test.bin', 23, 3)